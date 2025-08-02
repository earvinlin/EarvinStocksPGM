/*
 * gcc html_parser.c -o html_parser `pkg-config --cflags --libs libxml-2.0` -lcurl
 */


#include <stdio.h>
#include <stdlib.h>
#include <curl/curl.h>
#include <libxml/HTMLparser.h>
#include <libxml/xpath.h>
#include <string.h>

size_t write_callback(void *ptr, size_t size, size_t nmemb, void *userdata) {
    size_t total_size = size * nmemb;
    char **response_ptr = (char **)userdata;
    *response_ptr = strndup(ptr, total_size);
    return total_size;
}

void extract_links(const char *html) {
    htmlDocPtr doc = htmlReadMemory(html, strlen(html), NULL, NULL, HTML_PARSE_NOERROR | HTML_PARSE_NOWARNING);
    if (!doc) {
        fprintf(stderr, "Failed to parse HTML\n");
        return;
    }

    xmlXPathContextPtr xpathCtx = xmlXPathNewContext(doc);
    xmlXPathObjectPtr xpathObj = xmlXPathEvalExpression((xmlChar *)"//a/@href", xpathCtx);

    if (xpathObj && xpathObj->nodesetval) {
        xmlNodeSetPtr nodes = xpathObj->nodesetval;
        for (int i = 0; i < nodes->nodeNr; ++i) {
            xmlNodePtr node = nodes->nodeTab[i];
            if (node->type == XML_ATTRIBUTE_NODE) {
                printf("Link: %s\n", node->children->content);
            }
        }
    }

    xmlXPathFreeObject(xpathObj);
    xmlXPathFreeContext(xpathCtx);
    xmlFreeDoc(doc);
    xmlCleanupParser();
}

int main(void) {
    CURL *curl = curl_easy_init();
    char *html = NULL;

    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, "https://example.com");
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &html);
        CURLcode res = curl_easy_perform(curl);
        curl_easy_cleanup(curl);

        if (res == CURLE_OK && html) {
            extract_links(html);
            free(html);
        } else {
            fprintf(stderr, "Failed to fetch HTML\n");
        }
    }

    return 0;
}

