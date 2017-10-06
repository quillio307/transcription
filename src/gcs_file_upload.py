import logging
import os
import cloudstorage as gcs
import webapp2

from google.appengine.api import app_identity
def create_file(self, filename):
	"""Create a file.

  	The retry_params specified in the open call will override the default
  	retry params for this particular file handle.

  	Args:
    filename: filename.
	"""
	self.response.write('Creating file %s\n'%filename)
	write_retry_params = gcs.RetryParams(backoff_factor=1.1)
	gcs_file = gcs.open(filename,
                      'w',
                      content_type='text/plain',
                      options={'x-goog-meta-foo': 'foo',
                               'x-goog-meta-bar': 'bar'},
                      retry_params=write_retry_params)
	gcs_file.write('abcde\n')
	gcs_file.write('f'*1024*4 + '\n')
	gcs_file.close()
	self.tmp_filenames_to_clean_up.append(filename)

def main():
	create_file(self, "../test_audio_files/conversation_1.flac")

if __name__ == "__main__":
    main()