# Freelancer Job Board API

## Overview

The **Freelancer Job Board API** is structured using a relational database model optimized to **Third Normal Form (3NF)**. The API ensures **data integrity, avoids redundancy**, and maintains clear relationships between **freelancers, clients, jobs, applications, contracts, and reviews**.

## Features

- **User Management**: Freelancers and clients can register and manage their profiles.
- **Job Listings**: Clients can post jobs, and freelancers can browse available job opportunities.
- **Job Applications**: Freelancers can submit applications with bid amounts.
- **Contract System**: A formal agreement is created between a client and a freelancer upon job acceptance.
- **Review System**: After contract completion, both parties can leave reviews and ratings.


**Project GitHub Repo**: [Github Repository](https://github.com/TysonPWilliams/DEV-1002-Api-Project)

**Project Kanban Board**: [Kanban Board](https://github.com/users/TysonPWilliams/projects/8/views/1)

## Hosted API

The Freelancer Job Board API is live and accessible at:

🔗 **Base URL:** [https://tysonwilliams.dev](https://tysonwilliams.dev)

All API endpoints should be prefixed with this base URL. For example:
- `GET https://tysonwilliams.dev/jobs`
- `POST https://tysonwilliams.dev/users`

⚠️ Note: If the API doesn’t respond immediately, please wait 30-60 seconds while the server wakes up.



## Database Structure (Entities & Relationships)

### 1. Users (PK: `id`)

- Represents all **freelancers and clients**.
- **Attributes**: `name`, `email`, `address`, `role (freelancer/client/admin)`, `is_active`, `created_at`, `updated_at`.
- **Relationships**:
  - One-to-Many with **Jobs** → A client can post multiple jobs.
  - One-to-Many with **Contracts** → A freelancer can have multiple contracts.
  - One-to-Many with **Applications** → A freelancer can apply for multiple jobs.
  - One-to-Many with **Reviews** (through **Contracts**)→ Users can be reviewers or reviewees.

### 2. Jobs (PK: `id`)

- Represents **freelance job postings** created by clients.
- **Attributes**: `title`, `description`, `budget`, `status`, `created_at`, `is_active`, `client_id (FK → Users.id)`.
- **Relationships**:
  - One-to-Many with **Applications** → A job can receive multiple applications.
  - One-to-One with **Contracts** → A job can have **none or one** contract.

### 3. Applications (PK: `id`)

- Tracks **freelancers applying for jobs**.
- **Attributes**: `job_id (FK → Jobs.id)`, `freelancer_id (FK → Users.id)`, `bid_amount`, `status`, `created_at`.
- **Relationships**:
  - Many-to-One with **Jobs** → A job can have multiple applications.
  - Many-to-One with **Users (Freelancers)** → A freelancer can apply to multiple jobs.

### 4. Contracts (PK: `id`)

- Represents **formal agreements** between clients and freelancers.
- **Attributes**: `job_id (FK → Jobs.id)`, `freelancer_id (FK → Users.id)`, `client_id (FK → Users.id)`, `start_date`, `end_date`, `status`.
- **Relationships**:
  - One-to-One or One-to-Many with **Jobs** → A job may result in one or more contracts.
  - Many-to-One with **Users (Clients & Freelancers)**.
  - One-to-One with **Reviews** → A contract can have one review once completed.

### 5. Reviews (PK: `id`)

- Captures **ratings and feedback** from freelancers and clients after contract completion.
- **Attributes**: `contract_id (FK → Contracts.id)`, `rating`, `comment`, `created_at`.
- **Relationships**:
  - One-to-One with **Contracts** → A contract receives either **none** or **one** review upon completion.

---

## ⚙️ Setup Instructions

### 1. PostgreSQL Setup

- Download and install **PostgreSQL** from the [official website](https://www.postgresql.org/download/).
- Open **PostgreSQL** in your linux environment by running:

```sh
sudo -u postgres psql
```

- Create a new database and user

```sql
create database job_board_db;
create user job_board_dev with password 'secure_password';
```

- Grant ownership of the database to the new user and give all permissions
```sql
alter database job_board_db owner to job_board_dev;
grant all privileges on database job_board_db to job_board_dev;
grant all privileges on schema public to job_board_dev;
```

- Exit **PostgreSQL**
```shell
CTRL + Z
```
### 2. Create and Activate a Virtual Environment

```sh
python -m venv .venv
source .venv/bin/activate  # MacOS/Linux
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory and add your database connection string using your username, password, and database name. The host and port should be 127.0.0.1:8088

```ini
DB_URI = 'postgresql+psycopg2://<user>:<password>@<host>:<port>/<db name>'
```

### 5. Initialise the Database

```sh
flask db init
flask db seed  
```

### 6. Run the Flask Application

```sh
flask run
```

- The API should now be accessible at `http://127.0.0.1:8088/`

---

## 🛠 API Endpoints (Local Examples)

| Method | Endpoint          | Description         |
| ------ | ----------------- | ------------------- |
| `POST` | `/users`          | Register a new user |
| `POST` | `/jobs`           | Create a new job    |
| `GET`  | `/jobs`           | List all jobs       |
| `POST` | `/applications`   | Apply for a job     |
| `GET`  | `/contracts`      | View contracts      |
| `POST` | `/reviews`        | Submit a review     |

## 🛠 API Endpoints (Online Examples)

| Method | Endpoint          | Description         |
| ------ | ----------------- | ------------------- |
| `POST` | `https://tysonwilliams.dev/users`          | Register a new user |
| `POST` | `https://tysonwilliams.dev/jobs`           | Create a new job    |
| `GET`  | `https://tysonwilliams.dev/jobs`           | List all jobs       |
| `POST` | `https://tysonwilliams.dev/applications`   | Apply for a job     |
| `GET`  | `https://tysonwilliams.dev/contracts`      | View contracts      |
| `POST` | `https://tysonwilliams.dev/reviews`        | Submit a review     |

---
---

## 📜 License

This project is licensed under the **MIT License**.

---


