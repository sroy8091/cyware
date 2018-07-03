from rest_framework import serializers


class UserSearchSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=True)
    gt_repos = serializers.IntegerField(
        min_value=0, max_value=100000, required=False)
    lt_repos = serializers.IntegerField(
        min_value=0, max_value=100000, required=False)
    et_repos = serializers.IntegerField(
        min_value=0, max_value=100000, required=False)
    gt_followers = serializers.IntegerField(
        min_value=0, max_value=100000, required=False)
    lt_followers = serializers.IntegerField(
        min_value=0, max_value=100000, required=False)
    et_followers = serializers.IntegerField(
        min_value=0, max_value=100000, required=False)
    location = serializers.CharField(max_length=100, required=False)