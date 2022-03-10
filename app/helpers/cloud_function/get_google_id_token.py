import subprocess

def get_google_id_token():
    token = '{}'.format(subprocess.Popen(args="gcloud auth print-identity-token",
                        stdout=subprocess.PIPE, shell=True).communicate()[0])[2:-3]
    # print(token)
    return token
