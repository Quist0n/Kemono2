# Moderation System

## Table of contents
- [General Description](#general-description)
- [Interfaces](#interfaces)
- [Technical Description](#technical-description)
- [Process](#process)
- [Issues](#issues)

## General Description
The moderation system allows certain users ("moderators") chosen by the administrator user to perform various tasks.
Administrator can watch over all moderator and his own actions and selectively undo them if needed.
Administrator can visit his page and see various stats related to the site.
One of them allows to see the list of accounts and change their roles.

## Interfaces
```typescript
interface Account {
  id: string
  username: string
  password_hash: string
  created_at: Date
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
  type: "private" | "public"
  categories: string[]
  account_ids: string[]
  created_at: Date
  message: string
}

interface Action {
  id: string
  account_id: string
  type: string
  categories: string[]
  /**
   * A list of resource `id`s affected by the action.
   */
  entity_ids: string[]
  status: "completed" | "failed" | "reverted"
  created_at: Date
}
```

## Technical Description


## Process
### Administrator
1. The first registered user on an instance is going to be given the `"administrator"` role
1. At `/admin` the administrator arrives to the admin dashboard.
1. At `/admin/accounts` the administrator can change the roles of accounts, the list of which then gets sent to `POST` `/admin/accounts`.
1. The role change will result an `action` in `notifications` to related accounts.
1. At `/admin/accounts/<account_id>` the admin can see more detailed info for an account, and change its role too.
1. At `/admin/mods/actions` the admin can see the list of `actions` performed by mods, and at `POST` `/admin/mods/audit/search` filter them.

### Moderator
1. When the role of an account changes to `moderator`, the account gets notified of this.
1. The account then can access `/mod` endpoint, which leads to the moderator dashboard. On this page the mod can see various stats, among them is the list of various `tasks`.
1. Each performed `task` results in an `action`.

## Issues
