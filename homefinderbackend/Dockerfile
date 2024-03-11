#  the base image for our container
FROM python:3.12.0  

# set the working directory of the container
WORKDIR /homefinderbackend/main


# COPY ./requirement.txt /homefinderbackend/requirement.txt
# copy all files from the current directory
COPY . .

#  to install the dependencies
RUN pip install -r requirement.txt

# to specify the command,run when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
