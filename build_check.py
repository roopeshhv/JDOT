# Copyright (c) 2020 Nutanix Inc. All rights reserved.
#
# Author: roopesh.hv@nutanix.com
"""
Fetches the URL for latest smoke passed NOS build

"""

import json
import os
import re
import time


LATEST_NOS_COMMIT_URL = ("https://jita.eng.nutanix.com/api/v2/commits"
                         "/latest_smoke_passed?branch=%s&build_type=%s")

JITA_BUILD_URL = ("https://jita.eng.nutanix.com/api/v2/commits"
                  "/%s/build_url?build_type=%s")


def get_build_url(version, build_type="release"):
  """This routine fetches the build url for the latest smoke passed build.

  Args:
    version(str): The build version. Ex: 5.1.
    build_type(str): debug, opt, release

  Returns:
    (dict): Dict containing the build and metadata url.

  Raises:
      Error: Invalid NOS Type specified in config.json

  """
  assert build_type in ["release", "opt"]
  internal_build_name = "euphrates-%s-stable" % version
  latest_commit_url = LATEST_NOS_COMMIT_URL % (internal_build_name, build_type)
  response = os.popen("curl -k " + latest_commit_url).read()
  details = json.loads(response)
  commit_id = details["data"]["commit_id"]
  jita_build_url = JITA_BUILD_URL % (commit_id, build_type)
  response = os.popen("curl -k " + jita_build_url).read()
  details = json.loads(response)

  final_build_url = details.get("build_url")

  # Check if full download URL is available
  if not final_build_url:
    print "Could not build download URL as full_download_url not present for %s" % commit_id
    return {"tar_url": '', "nos_package": ''}
  print "Using NOS %s build %s at %s" % (
    internal_build_name, build_type, final_build_url)

  return {"tar_url": final_build_url,
          "nos_package": final_build_url.split("/")[-1]}



def check_nos_availability(available_images, nos_name):
  """
  This routine checks if NOS already present in FVM.
  """
  return nos_name in available_images


def check_hypervisor_availability(available_images, fname, hyp_type):
  """
  This routine checks if a given hypervisor is present in given list of images
  in FVM.

  Args:
    available_images(str): JSON of response of enumerating hypervisors in FVM.
    fname(str): Name of file to be searched in response.
    hyp_type(str): Hypervisor type.

  Returns:
    (boolean): True if it is present, False otherwise.

  """
  for i in available_images.get(hyp_type, ""):
    if i["filename"] in fname:
      return True
  return False

