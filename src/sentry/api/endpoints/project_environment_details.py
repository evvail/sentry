from __future__ import absolute_import

from rest_framework import serializers
from rest_framework.response import Response

from sentry.api.bases.project import ProjectEndpoint
from sentry.api.exceptions import ResourceDoesNotExist
from sentry.api.serializers import serialize
from sentry.models import EnvironmentProject


class ProjectEnvironmentSerializer(serializers.Serializer):
    isHidden = serializers.BooleanField()


class ProjectEnvironmentDetailsEndpoint(ProjectEndpoint):
    def get(self, request, project, environment):
        try:
            instance = EnvironmentProject.objects.select_related('environment').get(
                project=project,
                environment__name='' if environment == 'none' else environment,
            )
        except EnvironmentProject.DoesNotExist:
            raise ResourceDoesNotExist

        return Response(serialize(instance, request.user))

    def put(self, request, project, environment):
        try:
            instance = EnvironmentProject.objects.select_related('environment').get(
                project=project,
                environment__name='' if environment == 'none' else environment,
            )
        except EnvironmentProject.DoesNotExist:
            raise ResourceDoesNotExist

        serializer = ProjectEnvironmentSerializer(data=request.DATA, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        data = serializer.object
        fields = {}

        if 'isHidden' in data:
            fields['is_hidden'] = data['isHidden']

        if fields:
            instance.update(**fields)

        return Response(serialize(instance, request.user))
