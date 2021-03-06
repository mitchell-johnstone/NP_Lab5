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
The premise of this lab is to send an http GET request to a certain resource and expect 
a response on the HTTP port (or HTTPS port based on the link). Then, parse the status line
of the response, returning the status code of the response. Next, parse the headers of the
message to determine whether the response has a Transfer-Encoding of 'chunked' or a 
Content-Length otherwise. Parse the message body based on whether the body should be read
as a chunked response or not. Write the body into text files of the given filename.
Note: All of the bytes in this file should be interpreted as ASCII characters because this 
is an HTTP response.

Summary: (Summarize your experience with the lab and what you learned)
======================================================================
Through this lab, we struggled a bit in the beginning to organize the code in a way that
flowed between the methods well. After a bit of tinkering and brainstorming, we realized
the reading and parsing of the message had to be done concurrently, as the length of the
message was indeterminate without parsing out the whole message. After reformatting some
of the method functions, it was straightforward on how to split up tasks and receive the
response. We learned a lot about how http requests and responses are formatted in order
to be sent and received properly, with the status line, headers, and body encoding.


Feedback: (Describe what you liked, what you disliked, and any suggestions
you have for improvement) (required)
==========================================================================
Overall it was a fun exercise. I liked how this lab flowed well from the other TCP labs,
as the HTML request was just sending a TCP message in a specific format. The explanation
of the HTTPS could be better explained, because HTTP is explored in depth, but how to get
from HTTP to HTTPS is a bit fuzzy, especially with the ssl wrapper and the specific port.

"""

# import the "socket" module -- not using "from socket import *" in order to
# selectively use items with "socket." prefix
import socket

# import the "regular expressions" module
import re # https://docs.python.org/3/library/re.html

import ssl # for the HTTPS


def main():
    """
    Tests the client on a variety of resources
    """

    # These resource request should result in "Content-Length" data transfer
    get_http_resource('https://www.httpvshttps.com/check.png', 'check.png')

    # this resource request should result in "chunked" data transfer
    get_http_resource('https://milwaukee.craigslist.org/','index.html')
    
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
    secure = False
    if url[:7] == 'http://':
        url_match = re.search('http://([^/:]*)(:\d*)?(/.*)', url)
    else:
        url_match = re.search('https://([^/:]*)(:\d*)?(/.*)', url)
        secure = True
    match_groups = url_match.groups() if url_match else []
    #    print 'match_groups=',match_groups
    if len(match_groups) == 3:
        host_name = match_groups[0]
        host_port = int(match_groups[1][1:]) if match_groups[1] else (443 if secure else 80)
        host_resource = match_groups[2]
        print('host name = {0}, port = {1}, resource = {2}'
              .format(host_name, host_port, host_resource))
        status_string = do_http_exchange(host_name.encode(), host_port,
                                         host_resource.encode(), secure, file_name)
        print('get_http_resource: URL="{0}", status="{1}"'
              .format(url, status_string))
    else:
        print('get_http_resource: URL parse failed, request not sent')


def do_http_exchange(host, port, resource, secure, file_name):
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
    :author: Mitchell Johnstone
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

    # setting up the TCP Socket for sending and receiving http requests and responses.
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server.connect((host, port))

    # Wrapping the socket in a ssl wrapper for https
    if secure:
        context = ssl.create_default_context()
        tcp_server = context.wrap_socket(tcp_server, server_hostname=host.decode())

    # sending the http request
    request_line = b'GET ' + resource + b' HTTP/1.1\r\nHost: ' + host + b'\r\n\r\n'
    tcp_server.sendall(request_line)

    return parse_message(tcp_server, file_name)  # Replace this "server error" with the actual status code


"""OVERALL MESSAGE HANDLING"""
# Transfer-Encoding: chunked\r\n
# Content-Length: 193\r\n
def parse_message(data_socket, filename):
    """
    handle receiving and parsing the message. Gets the status code from the status line,
    reads through the headers to determine if the message is chunked or not, and writes the payload
    to the output file.
    :param data_socket: the tcp socket from which to read the http response.
    :param filename: the file to write the payload to.
    :return: the status code of the http response.
    :author: Mitchell Johnstone
    """

    # Get the status code
    status_code = read_status_line(data_socket)

    print(status_code)
    # Reading through the headers, getting vital information
    content_length, is_chunked = read_headers(data_socket)

    # Read the message, based off the encoding from the headers
    message = parse_body(data_socket, is_chunked, content_length)

    # write the interpreted message to a file.
    write_to_file(message, filename)

    return status_code


def read_line(data_socket):
    """
    Reads the next line of the message.
    :param data_socket: the socket to read the message from (passed to next_byte method)
    :return: The next line of the message, up to and including the '\n' character
    :author: Jonathan Keane
    """
    message = b''
    while message[-2:] != b'\r\n':
        current_char = next_byte(data_socket)
        message += current_char
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


"""STATUS LINE"""
def read_status_line(data_socket):
    """
    Reads the status line, returns back the status code
    :param data_socket: socket to read response data from
    :return: the status code
    :author: Mitchell Johnstone
    """
    return int(read_line(data_socket).split(b' ')[1])


"""HEADER INTERPRETATION"""
def read_headers(data_socket):
    """
    Should go through all the headers, checking if the body is
    chunked or length-oriented.
    :param data_socket: the socket to read the message from (passed to next_byte method)
    :return: the content length value and the whether the transfer encoding is chunked
    :author: Jonny Keane
    :editor: Mitchell Johnstone
    """
    headers_dict = {}
    current_line = read_line(data_socket)
    while len(current_line) != 2:
        header_name, header_value = get_header_name_value(current_line)
        headers_dict[header_name] = header_value
        current_line = read_line(data_socket)
    print(headers_dict)
    if b'Transfer-Encoding' in headers_dict.keys() and headers_dict[b'Transfer-Encoding'] == b'chunked':
        return 0, True
    return int(headers_dict[b'Content-Length']), False


def get_header_name_value(line):
    """
    reads the header and interprets the key and value.
    :param line: a header from the http request, as a bytes literals
    :return: a tuple (name, value) where name is the key of the header
    and value is the value of the header, both bytes literals.
    :author: Jonny Keane
    """
    name_value_split = line.decode()[:len(line)-2].split(': ')
    name = name_value_split[0].encode()
    value = name_value_split[1].encode()
    return name, value


"""BODY READING"""
def parse_body(data_socket, is_chunked=False, content_length=0):
    """
    Get the bytes that represent the message in the body
    Excludes extra bytes if it is a chunked response
    Otherwise, evaluates the body as one big piece based off of content length
    :param data_socket: the socket to read the message from (passed to next_byte method)
    :param is_chunked: whether the response is chunked or not
        :default False: method has to specifically call the body chunked through the parameter to activate this 
    :param content_length: the content length that will be used if the response is not chunked
        :default 0: if the response is chunked, the default allows the method to be called without the extra parameter
    :return: bytes object that represents the whole body message
    :author: Jonny Keane
    """
    message = b''
    if is_chunked:
        current_chunk_size = get_chunk_size(read_line(data_socket))
        while current_chunk_size:
            message += get_payload(data_socket, current_chunk_size)
            next_byte(data_socket) #CR
            next_byte(data_socket) #LF
            current_chunk_size = get_chunk_size(read_line(data_socket))
    else:
        message = get_payload(data_socket, content_length)
    return message


def get_chunk_size(bytes_): 
    """
    Clips off the last two bytes and cast as hexadecimal int
    :param bytes_: the bytes that represent the chunk size with CR LF attached
    :return: the decimal size of the chunk
    :author: Jonny Keane
    """
    return int(bytes_[:-2], 16)


def get_payload(data_socket, size):
    """
    Get a payload from the given data socket that has a length of size
    :param data_socket: the socket to read the message from (passed to next_byte method)
    :param size: the expected number of bytes in the payload
    :return: a bytes object that contains the payload (ASCII characters)
    :author: Jonny Keane
    """
    payload = b''
    for i in range(0, size):
        payload += next_byte(data_socket)
    return payload

"""FILE WRITING"""
def write_to_file(message, file_name):
    """
    writes the given message to the given file
    :param message: bytes literal of the payload of the http request
    :param file_name: the file to write the message to
    :author: Mitchell Johnstone
    """
    with open(file_name, "wb") as open_file:
        open_file.write(message)
    open_file.close()


main()
