import os

import click
import requests


@click.command()
@click.argument("domain")
@click.argument("user")
@click.argument("password")
def upload_unicor_imgs(domain, user, password):
    BASE_URL = f"https://{domain}/api/v1"

    # get token
    response = requests.post(
        f"{BASE_URL}/login", data={"username": user, "password": password}
    )
    if response.status_code != 200:
        print("ERROR: login error", response.text)
        return
    access_token = response.json().get("access_token")

    response = requests.get(f"{BASE_URL}/universities/unicor/buildings")

    for building in response.json():
        print("\n")
        # get images from folder called equals to building code
        path = os.path.join(
            os.path.dirname(__file__), "ubicor_imgs", building.get("code")
        )
        if not os.path.exists(path):
            print("does not exists", building.get("code"), building.get("name"))
            continue

        print(
            "------ upload imgs from building:",
            building.get("code"),
            " -------",
        )

        images = []
        for img_name in os.listdir(path):
            img_path = os.path.join(path, img_name)
            images.append((img_name, open(img_path, "rb")))

        response = requests.post(
            url=f"{BASE_URL}/universities/unicor/buildings/{building.get('id')}/images/",
            headers={"Authorization": f"Bearer {access_token}"},
            files=[("files", f) for f in images],
        )

        for img_name, image in images:
            image.close()

        print("upload", [i[0] for i in images])
        print("response code", response.status_code)
        if response.status_code != 201:
            print("response body:", response.text)
