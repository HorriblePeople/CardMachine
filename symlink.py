import subprocess, platform, os

src_sym = raw_input("Source directory for symlink: ")
tar_sym = raw_input("Target for symlink: ")
print src_sym, tar_sym
if not os.path.exists(src_sym):
    print "{} does not exist".format(src_sym)
elif not os.path.exists(tar_sym):
    print "{} does not exist".format(tar_sym)
else:
    system = platform.system()
    if system == "Windows":
        link_name = os.path.basename(tar_sym.strip('\\'))
        subprocess.Popen(["mklink",
                          "/D" if os.path.isdir(tar_sym) else "",
                          src_sym,
                          tar_sym],
                         shell=True,
                         cwd=src_sym,
                         stdout=subprocess.PIPE).stdout.read()
    elif system == "Linux":
        os.symlink(src_sym, tar_sym)
