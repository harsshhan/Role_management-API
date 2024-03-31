# TaskGuardian API Documentation

This document provides detailed documentation for the TaskGuardian API. TaskGuardian is a backend program built using FastAPI that allows users to manage tasks and user profiles.

## Endpoints

### Add New User by Admin

Adds a new user to the system by an admin user.

- **URL:** `/admin/newuser/{admin_uid}`
- **Method:** `POST`
- **Request Body:**
    - `name` (string, required): The name of the new user.
    - `email` (string, required): The email of the new user.
    - `role` (string, required): The role of the new user (e.g., admin, manager, user).

### Update User by Admin

Updates an existing user's profile information by an admin user.

- **URL:** `/admin/updateuser/{admin_uid}/{user_id}`
- **Method:** `PUT`
- **Request Body:**
    - `name` (string, optional): The updated name of the user.
    - `email` (string, optional): The updated email of the user.
    - `role` (string, optional): The updated role of the user.

### Delete User by Admin

Deletes an existing user from the system by an admin user.

- **URL:** `/admin/{admin_uid}/{user_id}`
- **Method:** `DELETE`

### Create Task

Creates a new task in the system.

- **URL:** `/create_tasks/{user_id}`
- **Method:** `POST`
- **Request Body:**
    - `task_id` (string, required): The ID of the task.
    - `task` (string, required): The name or description of the task.
    - `deadline` (string, required): The deadline for completing the task.
    - `assigned_to` (string, required): The ID of the user to whom the task is assigned.
    - `status` (string, required): The status of the task (e.g., pending, completed).

### Edit Task

Edits an existing task in the system.

- **URL:** `/edit_task/{user_id}/{task_id}`
- **Method:** `PUT`
- **Request Body:**
    - `task` (string, optional): The updated name or description of the task.
    - `deadline` (string, optional): The updated deadline for completing the task.
    - `assigned_to` (string, optional): The updated ID of the user to whom the task is assigned.
    - `status` (string, optional): The updated status of the task.

### Show Tasks

Retrieves tasks assigned to a user.

- **URL:** `/tasks/{user_id}`
- **Method:** `GET`
- **Response:** List of tasks assigned to the user.

## Error Handling

The API returns appropriate HTTP status codes and error messages for various scenarios, such as invalid input or unauthorized access.

## Authentication

The API endpoints are protected, and certain operations require authentication using user IDs and roles.

