
# Project Documentation

## Prerequisites

- Docker
- Docker Compose

## Setup

To build and start the project, simply run:

```bash
docker-compose up --build
```

If you have been built:

```bash
docker-compose up
```

If you want to use https:

- **Please read How_to_set_private_ssl and create key for this project**

```bash
docker-compose --file docker-compose_https.yml up
```

## Predefined Users

The following four users are pre-configured in the system with identical credentials:

- **Username**: `manager`, `FE`, `NE`, `ONC`
- **Password**: `as same as username`
- **Roles**:
  - `manager`: Admin user with full privileges.
  - `FE`: Frontend user.
  - `NE`: Network user.
  - `ONC`: Oncology user.

These accounts are created during the `docker-compose up --build` process.

## Adding New Users

To add a new user, you can use the provided `create_user.sh` script. Follow these steps:

1. Open the `create_user.sh` script.
2. Modify the parameters in the script:
   - **Username**: The new user's username.
   - **Password**: The new user's password.
   - **Role**: The new user's role. Valid options are `FE`, `NE`, `ONC`, and `admin`.

3. Run Server with docker, them run the script to create the new user:

   ```bash
   bash create_user.sh
   ```

   This will create the user and assign them the specified role.

### Valid Roles

- `FE`: Frontend user.
- `NE`: Network user.
- `ONC`: Oncology user.
- `admin`: Admin user with full access.

**Note**: Only the roles `FE`, `NE`, `ONC`, and `admin` are allowed. Make sure to set the role carefully when creating a new user.

## API Endpoints

## Notes

- If you need to modify user data, you can directly interact with the backend or modify the database.

- If you need to modify client sales daata, you can modify the static.csv file where in ./static.

## Troubleshooting

- If you encounter issues with Docker Compose, try running `docker-compose down` to stop and remove the containers, and then `docker-compose up --build` again.

- If you wnat check the source of volume, use `docker inspect merck_frontend-backend-1 | grep "Source"`

- Make sure files that you want mount have correct permission. You can check permission by `ll`. You may want to modify that with `chmod 744 <file>` or `chmod -R 744 <dict>`
  - (replace 744 with 766 or (777), it will make anyuser has modify permission (and execute permission ))
