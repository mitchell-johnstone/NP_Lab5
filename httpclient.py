"""
- CS2911 - 051
- Fall 2020
- Lab 5
- Names:
  - 
  - 

A simple HTTP client

Introduction: (Describe the lab in your own words)




Summary: (Summarize your experience with the lab and what you learned)


Feedback: (Describe what you liked, what you disliked, and any suggestions
you have for improvement) (required)





"""

# import the "socket" module -- not using "from socket import *" in order to
# selectively use items with "socket." prefix
import socket

# import the "regular expressions" module
import re


def main():
    """
    Tests the client on a variety of resources
    """

    # These resource request should result in "Content-Length" data transfer
    get_http_resource('http://www.httpvshttps.com/check.png', 'check.png')

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

    """
    Gotta do work here!
    Edit to make it run.
    function go brrrr
    """
 
    return 500  # Replace this "server error" with the actual status code

def ASCII_and_you_shall_receive_LOL():
    return
def parse_message(response, filename):
    pass
# Define additional functions here as necessary
# Don't forget docstrings and :author: tags


main()
