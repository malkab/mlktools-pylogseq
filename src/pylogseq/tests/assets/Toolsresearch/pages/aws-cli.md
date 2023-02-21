- #procesar

# AWS cli

Install:

```Shell
pip3 install awscli
```

At the development machine is also nice to have:

```Shell
pip3 install aws-shell
```



## Installing Credentials

Go to AWS Management Console and create a role, group, user, etc. Take note of the user **Access Key ID** and **Secret Access Key**. The run:

```Shell
aws configure
```

and answer the questions. Remember that the Ireland region is called **eu-west-1**.
