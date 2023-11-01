import replicate


def describe_image(moodboard):
    try:
        output = replicate.run(
            "methexis-inc/img2prompt:50adaf2d3ad20a6f911a8a9e3ccf777b263b8596fbd2c8fc26e8888f8a0edbb5",
            input={"image": open("path/to/file", "rb")}
        )
        description = ""
        for item in output:
            description += item
        return  description
    except:
        return ''

