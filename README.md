# update_staging
Update selected tables from live site to staging on DreamPress

Instructions:

clone the repository with:

```git clone https://github.com/cvzero89/update_staging```

move the py file to the root of the live site directory. Run with: 

```python3 update_staging.py```

How it looks like: 

```Site is domain.com.
If you're not running this from the live site, exit now.
Staging URL is domaincom.stage.site
The WordPress Prefix is wp_
List tables to update in staging separated with a space without the WordPress prefix: posts users
Tables to export wp_posts
Tables to export wp_users
Are the tables above correct?: [Y/N]
All good!
Success: Exported to 'wp_to_update_staging.sql'.
File wp_to_update_staging.sql moved to domaincom.stage.site. Changing directories.
Dropping tables wp_posts, wp_users.
Success: Imported from 'wp_to_update_staging.sql'. You can publish from staging now!
```
