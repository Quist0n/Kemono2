# Notifications

## Table of contents
- [General Description](#general-description)
- [Interfaces](#interfaces)
- [Technical Description](#technical-description)
- [Process](#process)
- [Issues](#issues)

## General Description
Notifications allow to send various information to users.

## Interfaces
### SQL Tables
```sql
    CREATE TABLE "UserSeenNotifications" (
        "Id" int8 NOT NULL,
        "UserId" int8 NOT NULL,
        "NotificationId" int8 NOT NULL,
        PRIMARY KEY ("Id")
    );
```

```sql
    ALTER TABLE "UserSeenNotifications" 
    ADD CONSTRAINT "UsersFK" 
    FOREIGN KEY ("UserId") 
    REFERENCES "Users" ("Id") 
    ON DELETE CASCADE;
```

```sql
    ALTER TABLE "UserSeenNotifications" 
    ADD CONSTRAINT "NotificationsFK" 
    FOREIGN KEY ("NotificationId") 
    REFERENCES "Notifications" ("Id") 
    ON DELETE CASCADE;
```

```sql
    CREATE UNIQUE INDEX "UsersNotificationsIdx" 
    ON "UserSeenNotifications" 
    USING btree (
        "UserId",
        "NotificationId"
    );
```

## Technical Description
## Process
## Issues
