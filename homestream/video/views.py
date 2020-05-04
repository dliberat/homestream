import os
import logging
import magic
import subprocess

from tempfile import NamedTemporaryFile

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.core.files import File

from video.models import VideoFile
from video.forms import VideoFileForm


logger = logging.getLogger(__name__)


@login_required
def index(request):
    videos = VideoFile.objects.order_by('-upload_date')[:50]
    ctx = {'videos': videos}
    return render(request, 'video/index.html', ctx)


@login_required
def watch(request, video_id):
    video = get_object_or_404(VideoFile, pk=video_id)
    return render(request, 'video/watch.html', {'video': video})


@login_required
@permission_required(('video.add_video_file', 'video.change_video_file'), raise_exception=True)
def video_upload(request):

    ctx = {'form': VideoFileForm()}

    if request.method == 'POST':
        form = VideoFileForm(request.POST, request.FILES)

        if form.is_valid():

            # Save the video file itself and metadata provided in the form
            vf = form.save()
            logger.info(f'Saved VideoFile at {vf.file_obj.path}')

            try:
                # Determine MIME type for playback
                mime = magic.Magic(mime=True)
                vf.mime_type = mime.from_file(vf.file_obj.path)

                # Generate thumbnail
                with NamedTemporaryFile(suffix='.jpg') as thumb:
                    subprocess.call([
                        'ffmpeg',
                        '-y', # overwrite existing jpg file
                        '-v', 'error', # reduce log output
                        '-i', vf.file_obj.path,
                        '-ss', '00:00:00.000',
                        '-vframes', '1',
                        thumb.name])
                    thumb_basename = os.path.basename(thumb.name)
                    vf.thumbnail.save(thumb_basename, File(thumb))

                # Update model with MIME data and thumbnail
                vf.save()

                ctx['video_id'] = vf.id

            except Exception:
                logger.error(f'Failed to determine MIME type or generate video thumbnail. \
                    Rolling back object creation', exc_info=True)
                vf.delete()

        else:
            ctx['form'] = form

    return render(request, 'video/upload.html', ctx)
