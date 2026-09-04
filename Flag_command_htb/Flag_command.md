# Flag Command challenge ~ HTB

So, the challenge is rated "Very Easy" and is based on the "Web" category. In this challenge, you
play a text based adventure game navigating through many different situations and choosing different
choices to advance forward.

But all challenges have a flag hidden somewhere right? So, in this challenge, I am probably looking
for some hidden flag within the server code, or somehow triggering the web-app to return the flag
when playing around with some inputs.

Upon entering the game I found this one string:

`Xclow3n`

Not really sure what it was, but moved ahead, and played the game normally just to get an idea of
how it functioned, how the game makes its decisions, what are the dead ends, etc.

After doing a little of gameplay, when I entered choices (the same ones that gave some story after
I clicked return), no story would come up and instead I would get the message:

`What are you trying to break`

So, here I thought it might be a dead end, and decided to see how the packets got sent to the
backend when I sent the commands. Interestingly, when I sent a command, this is the format it sent
it as:

```HTTP
POST http://154.57.164.68:30735/api/monitor HTTP/1.1
host: 154.57.164.68:30735
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Referer: http://154.57.164.68:30735/
Content-Type: application/json
content-length: 68
Origin: http://154.57.164.68:30735
Connection: keep-alive
Priority: u=0
```

```JSON
{"command":"HEAD NORTH"}
```
POST request, to the `/api/monitor` endpoint, and a clear key called "command" that takes the
command I enter directly to the server backend.

I captured the packets on `zaproxy` and modified them to send different commands, but nothing really
helped. Then, in one of the post requests, I got two sets of data, which has been attached for
viewing alongside this writeup in the same directory.

The `commands.js` I named as such because the endpoint from which I got the data was from
`/static/terminal/js/commands.js`.

That wasn't really interesting tho, what caught my attention, was the `options.txt` file
coming from the `/api/options`

It had a key called `secret`, so I tried entering that in the value space for the "command" key.

and viola!

Request payload:

```JSON
{"command":"Blip-blop, in a pickle with a hiccup! Shmiggity-shmack"}
```

Response:
```JSON
{
  "message": "HTB{D3v3l0p3r_t00l5_4r3_b35t__t0015_wh4t_d0_y0u_Th1nk??}"
}
```
