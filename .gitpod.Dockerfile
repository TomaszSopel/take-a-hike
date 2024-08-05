FROM gitpod/workspace-full
RUN curl https://cli-assets.heroku.com/install.sh 

# Install PostgreSQL
RUN sudo apt-get update && sudo apt-get install -y postgresql postgresql-contrib

# Setup PostgreSQL server for user gitpod
USER gitpod
RUN sudo /etc/init.d/postgresql start \
    && sudo -u postgres psql -c "CREATE USER gitpod WITH PASSWORD 'dbpassword';" \
    && sudo -u postgres psql -c "ALTER USER gitpod WITH SUPERUSER;" \
    && sudo -u postgres psql -c "CREATE DATABASE take_a_hike WITH OWNER gitpod;" \
    && sudo -u postgres psql -c "CREATE DATABASE take_a_hike_db WITH OWNER gitpod;"

