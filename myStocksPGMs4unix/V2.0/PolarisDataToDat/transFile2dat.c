#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void split(char **arr, char *str, const char *del) {
    char *s = strtok(str, del);
  
    while(s != NULL) {
        *arr++ = s;
        s = strtok(NULL, del);
    }
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

	/*
	 * ��춶�ǡG���,�}�L,�̰�,�̧C,���L, ����q, �ĸ�i��, �Ĩ�i��
	 */
//    in = fopen("2002-20170120.csv", "r");
//    out = fopen("2002-20170120.dat", "wb");
	char inputFileName[40] ;
	char outputFileName[40] ;
	char filePathCSV[] = "csv\\";
	char filePathDAT[] = "dat\\";
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
    out = fopen(outputFileName, "wb");

    while (fscanf(in, "%[^\n]\n", line) == 1) {
        printf("%s\n", line);
        split(arr, line, del);
        int i = 0;
        while(i < 8) {
//            printf("i= %d -- %.2f\n", i, atof(*(arr+i++)));
//            fprintf(out, "%f", atof(*(arr+i++)));
            f1 = atof(*(arr+i++));
            fwrite(&f1, sizeof(float), 1, out);
        }
    }

    fclose(in);
    fclose(out);

    return 0;
}

