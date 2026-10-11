# Lucky Dice

- Difficulty level: `Very Easy`

- given to us is a single python file that does the following:

![interface](/images/lucky_dice_1.png)

```text
NOTE: These points are written AFTER I completed the challenge.
(i) "Ready to play the game?"
(ii) 0.3 seconds answering time provided for user each round.
(iii) total of 100 rounds before we can get the flag from the server's directories labelled as "flag.txt"
```
The problem was, there was a very small wait time for me to enter a response, and it was annoying. So, I looked into the code and found this line that sets the `timeout`, and there was a check condition tied to this variable as well.

![code change #1](/images/code_change_1.png)

The timeout was still not actually helping, because the numbers list got increasing in size, and it was harder to compute. So I found this section of the code where it was printing the list of numbers. I modified it to print the sum of the number list as well.

![code change #2](/images/code_change_2.png)

It worked pretty well, but it looked like the calls were just going indefinetly. looking at the main loop executing the game loop, I found that there was a `rounds` variable controlling how many runs need to be done before retrieving the flag.

so I changed it from what it was originally, 100, to 1.

Ok, so now we're at this point in answering.
<Add the error png>
As can be seen, the file obiviously does not exist in the same directory. The target URL provided with a port, when scanned with nmap, does not specify the protocol on the port as well.

But one thing is clear. we need the `flag.txt` file to be in the same directory in order to retrieve its value.

So I tried typing out the `targetIP:port` in the address bar to see where it leads me to. But... got this instead:

<img of unsucessfull output>

I tried doing a `curl -X GET <ip_addr_target>` to see the type of headers I got. Perhaps I could make sense of the tech stack that this program was using. But didn't get anything.

I did a wireshark analysation of the HTTP request, Since as seen from the web output, I got automatically disconnected. Something in my requests was not allowing me to actually interface with the game. The `1` command, to start the game was automatically swapped with something else.

<wireshark output>

The different `continuation` outputs as seen (refer the web output to understand better) are directly tied to the rules and "Too bad... bye bye." messages.

Around this time, I found out that I have to connect to the server using a TCP socket connection, make a program and run it such that it receives the kind of inputs that the server needs and can automate the process of sending responses.

It was also around this time that I learnt I could use `netcat` in order to interface with webapps that I may not be able to directly connect in the browser.

In the end, I created a socket program to read the outputs from the `challenge.py` program running in the server, and send automated inputs from the client side (our machine) to the server. The program can be found in the same directory as this documentation file.

It just went away!

Eventually I got the flag :)



netcat-traditional download
automated VS code download
automatted Zapper download
