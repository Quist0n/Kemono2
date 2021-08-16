# Moderation System

## Table of contents
- [Interfaces](#interfaces)
- [Core information](#core-information)
- [Process](#process)
- [Issues](#issues)

## Interfaces
```typescript
interface Account {
  id: string
  username: string
  password: string
  created_at: Date | string
  role?: string | "consumer"
}

interface Administrator extends Account {
  role: "administrator"
}

interface Moderator extends Account {
  role: "moderator"
}

interface Notification {
  id: string
  /**
    A list of `account_id`s for the notification.
   */
  recipients: string
  created_at: Date | string
}

interface Action {
  id: string
  account_id: string
  type: string
  /**
   * A list of resource `id`s affected by the action.
   */
  created_at: Date | string
}
```

## Core information
The moderation system allows certain users ("moderators") chosen by the administrator user to perform various administrative tasks.

## Process
### Administrator
1. The first registered user on an instance is going to be given the `"administrator"` role
1. At `/admin` the administrator arrives to the admin dashboard.
1. At `/admin/accounts` the administrator can change the roles of accounts, the list of which then gets sent to `POST` `/admin/accounts`. Can filtered by `POST` `/admin/accounts/search`.
1. Presumably the role change will result in `notifications` to related accounts.
1. At `/admin/accounts/<account_id>` the admin can see more detailed info for an account, and change its role too.
1. At `/admin/mods/actions` the admin can see the list of `actions` performed by mods, and at `POST` `/admin/mods/audit/search` filter them.

### Moderator
1. When the role of an account changes to `moderator`, the account gets notified of this.
1. The account then can access `/mod` endpoint, which leads to the moderator dashboard. On this page the mod can see various stats, among them is the list of various `tasks`.
1. Each performed `task` results in an `action`.
## Issues
