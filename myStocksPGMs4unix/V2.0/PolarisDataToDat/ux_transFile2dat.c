#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
void split(char **arr, char *str, const char *del) {
    char *s = strtok(str, del);
  
    while(s != NULL) {
        *arr++ = s;
        s = strtok(NULL, del);
    }
}
*/
// 安全版本
int split(char **arr, char *str, const char *del, int max_fields) {
    int i = 0;
    char *s = strtok(str, del);
    while (s != NULL && i < max_fields) {
        arr[i++] = s;
        s = strtok(NULL, del);
    }
    return i;  // 回傳實際切割數
}

int main(int argc, char *argv[]) {

    FILE *in, *out;
    char line[80];
    const char *del = ",";

    char *arr[8];
    float *arr_f[8];
    float f1;

	if (argc != 2) {
		printf("Usage: %s filename\n", argv[0]);
		exit(EXIT_FAILURE);
	}

//    in = fopen("2002-20170120.csv", "r");
//    out = fopen("2002-20170120.dat", "wb");
	char inputFileName[40] ;
	char outputFileName[40] ;
	char filePathCSV[] = "csv/";
	char filePathDAT[] = "dat/";
	char filenameExtCSV[] = ".csv";
	char filenameExtDAT[] = ".dat";
	strcpy(inputFileName, filePathCSV);
	strcat(inputFileName, argv[1]);
	strcat(inputFileName, filenameExtCSV);
	printf("the input filename: %s\n", inputFileName);
	strcpy(outputFileName, filePathDAT);
	strcat(outputFileName, argv[1]);
	strcat(outputFileName, filenameExtDAT);
	printf("the output filename: %s\n", outputFileName);
	
	in = fopen(inputFileName, "r");
    if (in == NULL) {
        perror("無法開啟檔案");
        exit(EXIT_FAILURE);
    }
    out = fopen(outputFileName, "wb");
    if (out == NULL) {
        perror("無法開啟檔案");
        exit(EXIT_FAILURE);
    }

    while (fscanf(in, "%[^\n]\n", line) == 1) {
        printf("%s\n", line);
        int count = split(arr, line, del, 10);

        for (int i = 0; i < count; i++) {
            printf("data[%i]= %s\n", i+1, arr[i]);
//            printf("欄位 %d：%s\n", i + 1, fields[i]);
        }

        int i = 0;
        while(i < 8) {
            f1 = atof(*(arr+i++));
            fwrite(&f1, sizeof(float), 1, out);
        }
    }

    fclose(in);
    fclose(out);

    return 0;
}

