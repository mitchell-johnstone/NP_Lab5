"""
- CS2911 - 051
- Fall 2020
- Lab 5
- Names:
  - Jonny Keane
  - Mitchell Johnstone

A simple HTTP client

Introduction: (Describe the lab in your own words)
==================================================


Summary: (Summarize your experience with the lab and what you learned)
======================================================================


Feedback: (Describe what you liked, what you disliked, and any suggestions
you have for improvement) (required)
==========================================================================

"""

# import the "socket" module -- not using "from socket import *" in order to
# selectively use items with "socket." prefix
import socket

# import the "regular expressions" module
import re # https://docs.python.org/3/library/re.html


def main():
    """
    Tests the client on a variety of resources
    """

    # These resource request should result in "Content-Length" data transfer
    #get_http_resource('http://www.httpvshttps.com/check.png', 'check.png')

    # this resource request should result in "chunked" data transfer
    get_http_resource('http://www.httpvshttps.com/','index.html')
    
    # If you find fun examples of chunked or Content-Length pages, please share
    # them with us!


def get_http_resource(url, file_name):
    """
    Get an HTTP resource from a server
           Parse the URL and call function to actually make the request.

    :param url: full URL of the resource to get
    :param file_name: name of file in which to store the retrieved resource

    (do not modify this function)
    """

    # Parse the URL into its component parts using a regular expression.
    url_match = re.search('http://([^/:]*)(:\d*)?(/.*)', url)
    match_groups = url_match.groups() if url_match else []
    #    print 'match_groups=',match_groups
    if len(match_groups) == 3:
        host_name = match_groups[0]
        host_port = int(match_groups[1][1:]) if match_groups[1] else 80
        host_resource = match_groups[2]
        print('host name = {0}, port = {1}, resource = {2}'
              .format(host_name, host_port, host_resource))
        status_string = do_http_exchange(host_name.encode(), host_port,
                                         host_resource.encode(), file_name)
        print('get_http_resource: URL="{0}", status="{1}"'
              .format(url, status_string))
    else:
        print('get_http_resource: URL parse failed, request not sent')


def do_http_exchange(host, port, resource, file_name):
    """
    Get an HTTP resource from a server

    :param bytes host: the ASCII domain name or IP address of the server machine
                       (i.e., host) to connect to
    :param int port: port number to connect to on server host
    :param bytes resource: the ASCII path/name of resource to get. This is
           everything in the URL after the domain name, including the first /.
    :param file_name: string (str) containing name of file in which to store the
           retrieved resource
    :return: the status code
    :rtype: int
    """

    '''
    response = make_request()
        set up tcp socket (socket created here)
        send message based on http request header
        receive response
        return response
    parse_message(response, filename)
        decode bytes following ascii header guidelines
        parse_status_lines()
        decode_chunked_response()

        write to file
    '''
    status_code = parse_message_status_code(response.decode('ASCII'), "message_destination.txt")
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server.connect((host, port))
    request_line = b'GET ' + resource + b' HTTP/1.1\r\nHost: ' + host + b'\r\n\r\n'
    tcp_server.sendall(request_line)

    """
    Gotta do work here!
    Edit to make it run.
    function go brrrr.
    """
 
    return status_code  # Replace this "server error" with the actual status code

def ASCII_and_you_shall_receive_LOL():
    return

def parse_message_status_code(data_socket, filename):
    status_code = -1
    #SECTION ABOVE RESERVED FOR THE GETTING THE STATUS CODE
    content_length = -1:
    while True:
        current_line = get_next_line(data_socket)
        if get_content_length(current_line) != -1:
            content_length = get_content_length(current_line)
        if len(current_line) == 2:
            break
    message = read_body(data_socket, content_length)
    output_file = open(filename, 'wb')
    return status_code
    
def get_content_length(line):
    return -1

def read_line(data_socket):
    """
    Reads the next line of the message.
    :param data_socket: the socket to read the message from (passed to next_byte method)
    :return: The next line of the message, up to and including the '\n' character
    :author: Jonathan Keane
    """
    message = b''
    while True:
        current_char = next_byte(data_socket)
        message += current_char
        if message[-2:] == b'\r\n':
            return message

def next_byte(data_socket):
    """
    Read the next byte from the socket data_socket.
   
    Read the next byte from the sender, received over the network.
    If the byte has not yet arrived, this method blocks (waits)
      until the byte arrives.
    If the sender is done sending and is waiting for your response, this method blocks indefinitely.
   
    :param data_socket: The socket to read from. The data_socket argument should be an open tcp
                        data connection (either a client socket or a server data socket), not a tcp
                        server's listening socket.
    :return: the next byte, as a bytes object with a single byte in it
    """
    return data_socket.recv(1)


def parse_message(response, filename):
    pass
# Define additional functions here as necessary
# Don't forget docstrings and :author: tags

# message = 'This is a test\r\n\r\nI just want to see what happens'
# parse_message(message, '')

#------------------------------------------------------------------

# main()

#     response = b''

#     get_next_line(data_socket)
#     print(response.split('\r\n'))
#     header = decode()
#     for line in response.split('\r\n')[1:]:
#         if line != '':

#         else:
#             break

#     parse_chunked_response(data_socket)