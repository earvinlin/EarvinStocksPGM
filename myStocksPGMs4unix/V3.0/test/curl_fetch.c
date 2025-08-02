#include <stdio.h>
#include <stdlib.h>
#include <curl/curl.h>

// 寫入回呼函式
size_t write_callback(void *ptr, size_t size, size_t nmemb, FILE *stream) {
    return fwrite(ptr, size, nmemb, stream);
}

int main(void) {
    CURL *curl;
    FILE *fp;
    CURLcode res;
    const char *url = "https://example.com";
    const char *outfilename = "output.html";

    curl = curl_easy_init();
    if (curl) {
        fp = fopen(outfilename, "wb");
        if (!fp) {
            perror("Can't open output file");
            return 1;
        }

        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, fp);

        res = curl_easy_perform(curl);
        if (res != CURLE_OK)
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));

        fclose(fp);
        curl_easy_cleanup(curl);
    }

    return 0;
}

