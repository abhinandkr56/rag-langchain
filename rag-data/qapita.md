Hi i am talking about the migration team, 

# Migrator Console Application Documentation

## Overview
The `Migrator` console application is a tool designed for data migration from MyEsop to QMap. It facilitates this process through the use of Dapper for database operations, SQL queries, and QMap API calls. This document provides detailed instructions and command line options for effective use of the Migrator tool.

## Command Line Options

### Basic Migration
- **Command**: `Migrator -c [ClientDatabaseName]`
- **Description**: Initiates the migration process for the specified client database.

### Verification Only
- **Command**: `Migrator -c [ClientDatabaseName] -v`
- **Description**: Performs only data verification without migration.

### Data Masking
- **Command**: `Migrator -c [ClientDatabaseName] -h`
- **Description**: Masks original data for testing purposes during migration.

### Migrating Users Only
- **Command**: `Migrator -c [ClientDatabaseName] -u`
- **Description**: Migrates only the user data.

### Incremental Data Migration
- **Command**: `Migrator -c [ClientDatabaseName] -r all`
- **Description**: Performs incremental migration for picking up new data since the last migration.

#### Employee-wise Incremental Migration
- **Command**: `Migrator -c [ClientDatabaseName] -r emp/["emp1","empId2"]`
- **Description**: Performs incremental migration for specific employees.

### Migrating Specific MyEsop Editions
- **Default Edition**: ED 1.8
- **Command for ED 1.0**: `Migrator -c [ClientDatabaseName] -e Ed1.0`
- **Description**: Specifies the version of MyEsop to use during migration.

### Reverting Migration
- **Commands**:
    - For Employees: `Migrator -c [ClientDatabaseName] -d emp/["empid1","empid2"]`
    - For Grants: `Migrator -c [ClientDatabaseName] -d grant/["grantid1","grantid2"]`
- **Description**: Reverts migration for specified employees or grants, preserving stakeholder data.

### Applying Patches
- **Command**: `Migrator -c [ClientDatabaseName] -p`
- **Description**: Applies MyEsop patches.

### Parallel Migration
- **Command**: `Migrator -c [ClientDatabaseName] -j`
- **Description**: Executes migration with concurrency for faster processing.

### Data Mismatch Finder
- **Command**: `Migrator -c [ClientDatabaseName] -f`
- **Description**: Identifies and reports data mismatches.



## Documentations

- [Migration Process]



# Data Migration Process from MyESOP to QMap

## Detailed Process Steps

### Initial Client Selection
1. **Client Identification:**
   - The business team specifies which client to migrate.

### Migrating to the Migration Server
2. **Preparation for Migration:**
   - Migration must be initiated from the Support Server database and VM.
   - Backup and restore the database on the Support Server with the latest database from the production server by running the following script:
     ```sql
     exec ESOPManager..db_Backuptopreprod 'ClientName'
     ```
     (if this doesn't works, ask Aniket or Amit for help)

### Initial Data Checks
3. **Conducting Data Checks:**
   - Perform initial data checks using specific SQL scripts available in the Migration Tool's solution folder.
   - Identify issues and Fix it. Consult with Neha or Prachi for guidance on resolution if required.

### Data Migration to Migration Server
4. **Actual Migration:**
   - Proceed with data migration to the Migration Server.
   - Once the whole migration is completed, Use the validation script to identify any discrepancies in the vestwise and stakeholder personal details reports.
    ```
     Migrator -c ClientDatabaseName -v
     ```
   - Rectify any mismatches found by applying patches or consulting with the business team for further instructions.

### Preparation for Production
5. **Final Checks before Production Migration:**
   - Once the business team confirms data accuracy, work with Aniket to transfer essential documents (Grant letters, Logo, and other documents like Exericse forms, Esop Schemes, FAQ, Popups etc.) to the Migration VM.
   - This step is crucial to avoid omissions during the final migration.

### Migration to Production
6. **Migrating to Production:**
   - After migration, carry out thorough data verification and make necessary corrections.
   - The business team also conducts their review of the data.

### Going Live
7. **Pre-Live Steps:**
   - Correct exercise numbers by running the designated patch (CorrectExerciseNumber).
   - In cases of delayed go-live, handle incremental data migration to account for new data in MyESOP. Use:
     ```
     Migrator -c ClientDatabaseName -r all
     ```
     This command ensures only the new, unmigrated data is transferred. After this also, check for data mismatches and rectify it.

### Generating Exercise Forms
8. **Exercise Form Preparation:**
   - Acquire exercise form templates from Aniket or Vibhav.
   - Use the already existing utility (MyEsopSQLConnectorBuild) to transfer all exercises to the ESOP_FORM_GEN_REQUEST table. For further clarification, consult Aniket or Sagar.
   - Make sure `IsActivatedForExForm` column is enabled in the EsopManager database and set the `isProcessed` column in the ESOP_FORM_GEN_REQUEST table to `0`.
   - Run the Exercise Form Generation utility in the Migration VM(ExerciseFormGenerator-Build) with the client database name in the config file.

### Finalizing Exercise Forms
9. **Completion of Exercise Forms:**
   - On successful generation of exercise forms, store them in the designated folder and apply the 'attach exercise form' patch.
   - For pending exercises, it is required to add the Exercise form template. Because when employee updates the payment details, the forms should be generated automatically. Add the Exercise Form Template ID using the correct patch.