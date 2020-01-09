import pathlib

PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE_PATH = PROJECT_ROOT.joinpath("packaging", "templates")
DST_PATH = PROJECT_ROOT.joinpath(".github", "actions")

def generate():
  """
  Generate Github action files for generating .deb files for various debian based environments.
  We wanted to use --build-args to switch the base environments of dockerfiles, but `build-args` are not supported by Github actions. https://github.community/t5/GitHub-Actions/Feature-Request-Build-args-support-in-Docker-container-actions/td-p/37802
  We planed to migrate it to use build-args feature after Github support it.
  """
  images = [
    {
        "name": "bionic",
        "image_name": "ubuntu:bionic"
    },
    {
        "name": "eoan",
        "image_name": "ubuntu:eoan"
    },
    {
        "name": "stretch",
        "image_name": "debian:stretch"
    },
    {
        "name": "buster",
        "image_name": "debian:buster"
    },
  ]
  notification = ("# Do not modify this file directly.\n" +
                  "# This file is automatically generated from" +
                  " packaging/generate_actions.py\n")
  with open(TEMPLATE_PATH.joinpath("template.dockerfile"), 'r') as f:
    docker_template = f.read()
  with open(TEMPLATE_PATH.joinpath("template.yml"), 'r') as f:
    action_template = f.read()
  for image in images:
    with open(DST_PATH.joinpath(image["name"], "Dockerfile"), "w") as f:
      f.write(notification)
      f.write(docker_template.format(base_image=image["image_name"]))
    with open(DST_PATH.joinpath(image["name"], "action.yml"), "w") as f:
      f.write(notification)
      f.write(action_template.format(target=image["name"]))

if __name__ == "__main__":
  generate()
