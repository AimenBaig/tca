from django.contrib.sessions import serializers
from django.db import models


class tbl_users(models.Model):
    upload_location = 'profile_image'
    uid = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=60, blank=True, null=True)
    last_name = models.CharField(max_length=60, blank=True, null=True)
    email = models.EmailField(max_length=80, blank=True, null=True)
    password = models.CharField(max_length=60, blank=True, null=True)
    phone_no = models.CharField(max_length=60, blank=True, null=True)
    # designation_id = models.ForeignKey('tbl_designation', on_delete=models.CASCADE, blank=False, null=False)
    # HQ_id = models.ForeignKey('tbl_headquarter',  on_delete=models.CASCADE, blank=False, null=False)
    # role_id = models.ForeignKey('tbl_user_role', on_delete=models.CASCADE, blank=False, null=False)
    designation_id = models.IntegerField()
    HQ_id = models.IntegerField()
    role_id = models.IntegerField()
    photo = models.ImageField(upload_to='profile_image', null=True, blank=True,
                              default='profile_image/default_photo.png')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.IntegerField(blank=True, null=True)
    modified_at = models.DateTimeField(auto_now_add=True, blank=True)
    modified_by = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_users'

    def __str__(self):
        return self.uid

    @property
    def avatar(self):
        return self.photo

    @avatar.setter
    def avatar(self, value):
        self.photo = value


class tbl_api_setting(models.Model):
    api_id = models.AutoField(primary_key=True)
    api_key = models.CharField(max_length=120, blank=True, null=True)
    api_key_secret = models.CharField(max_length=120, blank=True, null=True)
    access_token = models.CharField(max_length=120, blank=True, null=True)
    access_token_secret = models.CharField(max_length=120, blank=True, null=True)
    setting_status = models.CharField(max_length=120, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.IntegerField(blank=True, null=True)
    modified_at = models.DateTimeField(auto_now_add=True, blank=True)
    modified_by = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_api_setting'

    def __str__(self):
        return self.api_key


class tbl_user_role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=120, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    created_by = models.IntegerField(blank=True, null=True)
    modified_at = models.DateTimeField(auto_now_add=True, blank=True)
    modified_by = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_user_role'

    def __str__(self):
        return self.role_id


class tbl_designation(models.Model):
    designation_id = models.AutoField(primary_key=True)
    designation = models.CharField(max_length=120, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.IntegerField(blank=True, null=True)
    modified_at = models.DateTimeField(auto_now_add=True, blank=True)
    modified_by = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_designation'

    def __str__(self):
        return self.designation_id


class tbl_messages(models.Model):
    msg_id = models.AutoField(primary_key=True)
    msg_subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    msg_attachment = models.CharField(max_length=120, blank=True, null=True)
    uid = models.IntegerField(blank=True, null=True)
    sender_id = models.IntegerField(blank=True, null=True)
    seen_status = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.IntegerField(blank=True, null=True)
    modified_at = models.DateTimeField(auto_now_add=True, blank=True)
    modified_by = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_messages'

    def __str__(self):
        return self.msg_subject


class tbl_reply_msg(models.Model):
    reply_id = models.AutoField(primary_key=True)
    msg_id = models.IntegerField(blank=True, null=True)
    reply = models.TextField(blank=True, null=True)
    seen_status = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.IntegerField(blank=True, null=True)
    modified_at = models.DateTimeField(auto_now_add=True, blank=True)
    modified_by = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_reply_msg'


class tbl_msg_draft(models.Model):
    draft_id = models.AutoField(primary_key=True)
    msg_subject = models.TextField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    uid = models.IntegerField(blank=True, null=True)
    sender_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.IntegerField(blank=True, null=True)
    modified_at = models.DateTimeField(auto_now_add=True, blank=True)
    modified_by = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_msg_draft'


class tbl_tweeter_users(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60, blank=True, null=True)
    username = models.CharField(max_length=60, blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    profile_url = models.CharField(max_length=255, blank=True, null=True)
    protection_status = models.BooleanField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    verification = models.BooleanField(blank=True, null=True)
    followers_count = models.IntegerField()
    friends_count = models.IntegerField()
    listed_count = models.IntegerField()
    favourites_count = models.IntegerField()
    statuses_count = models.IntegerField()
    profile_created_on = models.DateTimeField()
    profile_banner_url = models.CharField(max_length=255, blank=True, null=True)
    profile_image_url_https = models.CharField(max_length=255, blank=True, null=True)
    default_profile = models.BooleanField()
    default_profile_image = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        db_table = 'tbl_tweeter_users'


class tbl_tweets(models.Model):
    tweets_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    tweets = models.TextField()
    tweet_posted_date = models.CharField(max_length=100, blank=True, null=True)
    lang_code = models.CharField(max_length=10, blank=True, null=True)
    search_type = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        db_table = 'tbl_tweets'


class tbl_crime_categories(models.Model):
    cat_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.IntegerField(blank=True, null=True)
    modified_at = models.DateTimeField(auto_now_add=True, blank=True)
    modified_by = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_crime_categories'


class tbl_analysis(models.Model):
    analysis_id = models.AutoField(primary_key=True)
    tweet_id = models.CharField(max_length=1000, blank=True, null=True)
    tweet_text = models.CharField(max_length=1000, blank=True, null=True)
    tweet_link = models.CharField(max_length=1000, blank=True, null=True)
    username = models.CharField(max_length=1000, blank=True, null=True)
    polarity = models.CharField(max_length=1000, blank=True, null=True)
    subjectivity = models.CharField(max_length=1000, blank=True, null=True)
    profile_url = models.CharField(max_length=1000, blank=True, null=True)
    # tweets_id = models.IntegerField()
    # pos_sum = models.IntegerField()
    # pos_neg = models.IntegerField()
    # posCount = models.IntegerField()
    # negCount = models.IntegerField()
    # nullCount = models.IntegerField()
    # uid = models.IntegerField()
    analysis_status = models.CharField(max_length=255, blank=True, null=True)

    # created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        db_table = 'tbl_analysis'


class tbl_category_analysis(models.Model):
    cat_analysis_id = models.AutoField(primary_key=True)
    tweet_id = models.IntegerField()
    cat_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        db_table = 'tbl_category_analysis'


class tbl_headquarter(models.Model):
    HQ_id = models.AutoField(primary_key=True)
    hq_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField()
    phone_no = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.IntegerField(blank=True, null=True)
    modified_at = models.DateTimeField(auto_now_add=True, blank=True)
    modified_by = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_headquarter'

    def __str__(self):
        return self.HQ_id


class tbl_faked_account(models.Model):
    fake_account_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    suspicious_level = models.CharField(max_length=255, blank=True, null=True)
    tag_code = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        db_table = 'tbl_faked_account'


class tbl_hacked_account(models.Model):
    hacked_account_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    change_start_from = models.DateField()
    change_end_at = models.DateField()
    tag_code = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        db_table = 'tbl_hacked_account'


class tbl_system_setting(models.Model):
    system_setting_id = models.AutoField(primary_key=True)
    system_name = models.CharField(max_length=120, blank=True, null=True)
    system_logo = models.ImageField(upload_to='profile_image', blank=True, null=True,
                                    default='profile_image/twitter_logo.png')
    system_lang = models.CharField(max_length=120, blank=True, null=True)
    modified_by = models.IntegerField()
    modified_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        db_table = 'tbl_system_setting'

    def __str__(self):
        return self.system_name


class raw_tweets(models.Model):
    raw_tweet_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=120, blank=True, null=True)
    name = models.CharField(max_length=120, blank=True, null=True)
    location = models.CharField(max_length=120, blank=True, null=True)
    profile_url = models.CharField(max_length=120, blank=True, null=True)
    protected = models.CharField(max_length=120, blank=True, null=True)
    description = models.CharField(max_length=120, blank=True, null=True)
    is_verified = models.CharField(max_length=120, blank=True, null=True)
    follower_count = models.CharField(max_length=120, blank=True, null=True)
    friends_count = models.CharField(max_length=120, blank=True, null=True)
    listed_count = models.CharField(max_length=120, blank=True, null=True)
    favourites_count = models.CharField(max_length=120, blank=True, null=True)
    statuses_count = models.CharField(max_length=120, blank=True, null=True)
    profile_created_at = models.CharField(max_length=120, blank=True, null=True)
    profile_banner_url = models.CharField(max_length=120, blank=True, null=True)
    profile_image_url_https = models.CharField(max_length=120, blank=True, null=True)
    default_profile = models.CharField(max_length=120, blank=True, null=True)
    default_profile_image = models.CharField(max_length=120, blank=True, null=True)
    tweet_text = models.TextField(blank=True, null=True)
    tweet_posted_date = models.CharField(max_length=120, blank=True, null=True)
    lang_code = models.CharField(max_length=120, blank=True, null=True)
    tweet_source = models.CharField(max_length=120, blank=True, null=True)
    search_type = models.CharField(max_length=120, blank=True, null=True)

    # created_at = models.DateTimeField(auto_now_add=True, blank=True)
    # created_by = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_raw_tweets'

    def __str__(self):
        return self.name


class tbl_train_dataset(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=120, blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_train_dataset'

    def __str__(self):
        return self.id


class tbl_raw_analysis(models.Model):
    analysis_id = models.AutoField(primary_key=True)
    tweet_id = models.CharField(max_length=1000, blank=True, null=True)
    tweet_text = models.CharField(max_length=1000, blank=True, null=True)
    tweet_link = models.CharField(max_length=1000, blank=True, null=True)
    username = models.CharField(max_length=1000, blank=True, null=True)
    polarity = models.CharField(max_length=1000, blank=True, null=True)
    subjectivity = models.CharField(max_length=1000, blank=True, null=True)
    profile_url = models.CharField(max_length=1000, blank=True, null=True)
    analysis_status = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'tbl_raw_analysis'
