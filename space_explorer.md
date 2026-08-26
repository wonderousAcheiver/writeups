# Space Explorer challenge HTB
===========================
Quick pre-requisite notes:

- */dev/null* folder is also known as the "void folder", because anything sent to this folder is instantly removed
from the system. Anything to be tried and read from the void folder, will return an EOF error.

- The *FROM* command added before a version of a tool or package sets the stage for what the subsequent commands must
use in order to run their commands.
===========================
# DockerFile dissection

## Directory structure live updating and command explanations:

> /usr/src/go-getter
             |_go.mod
             |_go.sum

*RUN go mod download* essentially downloads the dependencies and libraries required to run the go file. If the
contents of the mod file haven't changed, then the one from the cache is used instead for referencing.

> /usr/src/go-getter
             |_go.mod
             |_go.sum
	     |_main.go

The command: *RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping*
tells the image to run with Host OS C-libraries dependencies as disabled, go build image to be run as linux based
executable, final go build binary to be stored under the name of "docker-gs-ping"
A copy of the binary executable is stored in the "go-builder" location, which is disposed once the docker build is
complete. 

> /usr/src
	|_go-getter
		|_go.mod
		|_go.sum
		|_main.go
	|_python-service
		|_app.py
		|_entrypoint.sh

> /usr/local/bin
	      |_docker-gs-ping (linux based executable)

ENV variable "FLAG" is set to some HTB{...} value, port 8080 is exposed (open, but with nothing to broadcast, yet),
entrypoint.sh is the file which should run by default when this container is started.

# entrypoint.sh file dissection

> set -e

Set's the first "Law" of the program, that if at all anything goes wrong during execution and runtime, exit the
program immediately.

# cleanup() {
#    kill -TERM "$GUNICORN_PID" "$GOAPP_PID" 2>/dev/null
# }
# trap cleanup TERM INT

"if the user pressed Ctrl+C for whatever reason, find those workers with the GUINCORN_PID process ID variable(s) 
I give you and the GoAPP_ID process ID and gracefully shut them down, as well as clean up the mess"

INT being "interuppt" and TERM being a system signal, trap command catches these signals and executes a user-defined
function to execute on encounter.

> python -m gunicorn --workers 4 -b 127.0.0.1:8081 app:app &

python asks gunicorn library to execute the following command of creating for worker processes and bind them to the
localhost IP addr & port 8081. in "app:app &", the first "app" is "app.py" file, and the second "app" is the name
of the flask app we've created for easier reference, the "&" tells python to run the whole process in the background

> GUNICORN_PID=$!

the "$!" command in bash is to check the process ID of the process just run before it. and we've stored the result in
the "GUNICORN_PID" variable.

The same goes with GOAPP_PID=$! written after running the docker-gs-ping linux executable

> wait -n "$GUNICORN_PID" "$GOAPP_PID" 
wait until one of those process are terminated, if you detect it, break out of that wait loop.
> cleanup
cleanup...
> wait
wait until the cleanup process is complete (here).


# Running the build-docker.sh file:

- upon running the file, docker image built successfully and the webapp was launched in localhost under port 8080.

upon changing the port in entrypoint.sh from 8081 to 8080, the app built successfully, started running, and exited 
immediately. Why?

I tried looking into ways of cracking the flag for 3 days now, and I finally decided to get my first hint from a writeup. Apparently, the way GO and python view json files (in this challenge) is different. There is a specific GO method 
that checks the action variable as case-insensitive, while that in python being case-sensitive because it uses dictionaries.

The above line for my explanation might be completely wrong, but eitherways, I tried entering the below command then just to see what happens:

> curl -X POST -H "Content-Type: application/json" -d '{"action":"getSecureCode", "Action":"getcosmic"}' "http://127.0.0.1:8080/execute"

and what do you know...

{"flag":"HTB{f4k3_fl4g_4_t3st1ng}","name":"Captain's Log","src":"https://images.unsplash.com/photo-1534447677768-be436bb09401?w=600"}

But, looking at this flag, I found the same flag in the dockerFile in the beginning itself...
