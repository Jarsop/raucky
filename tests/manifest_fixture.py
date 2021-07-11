"""
Manifest stubs for testing manifest class
"""

MANIFEST = """[update]
compatible=raucky
version=1.0
description=GeneratorVersion=1.1
build=20210711100221

[image.rootfs]
sha256=e1dd87c830c2ee711883cb88472ba5a01a9254f82450d11aafa7086445106894
size=6
filename=rootfs.img

"""

MANIFEST_TO_UPDATE = """[update]
compatible=raucky
version=1.0
description=GeneratorVersion=1.1
build=20210711100221

[image.rootfs]
sha256=
size=
filename=rootfs.img

"""

MANIFEST_WITHOUT_UPDATE = """[image.rootfs]
sha256=
size=
filename=rootfs.img

"""

MANIFEST_WITHOUT_IMAGE_ROOTFS = """[update]
compatible=raucky
version=1.0
description=GeneratorVersion=1.1
build=20210711100221

"""

MANIFEST_WITH_HOOK = """[update]
compatible=raucky
version=1.0
description=GeneratorVersion=1.1
build=20210711100221

[hooks]
filename=hook.sh

[image.rootfs]
sha256=e1dd87c830c2ee711883cb88472ba5a01a9254f82450d11aafa7086445106894
size=6
filename=rootfs.img

[image.bootloader]
sha256=fe7dbbfd860ac700911244a54f68c48d510fa7d453f147d918548ee20d810c91
size=10
filename=bootloader.img
hooks=install;

"""

MANIFEST_WITH_HOOK_TO_UPDATE = """[update]
compatible=raucky
version=1.0
description=GeneratorVersion=1.1
build=20210711100221

[hooks]
filename=hook.sh

[image.rootfs]
sha256=
size=
filename=rootfs.img

[image.bootloader]
sha256=
size=
filename=bootloader.img
hooks=install;

"""

IMAGE_ROOTFS = "RootFS"

IMAGE_BOOTLOADER = "Bootloader"

HOOK = "hook"
