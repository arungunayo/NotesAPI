#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

// Word Count
int wordcount(char *text) {
    int count = 0;
    int inWord = 0;
    for (int i = 0; text[i] != '\0'; i++) {
        if (isspace((unsigned char)text[i])) {
            if (inWord) {
                count++;
                inWord = 0;
            }
        } else {
            inWord = 1;
        }
    }
    if (inWord) count++;
    return count;
}

// Caesar Cipher
void encrypt(char *text, int shift) {
    for (int i = 0; text[i] != '\0'; i++) {
        if (isalpha((unsigned char)text[i])) {
            char base = isupper(text[i]) ? 'A' : 'a';
            text[i] = (text[i] - base + shift) % 26 + base;
        }
    }
}

void decrypt(char *text, int shift) {
    for (int i = 0; text[i] != '\0'; i++) {
        if (isalpha((unsigned char)text[i])) {
            char base = isupper(text[i]) ? 'A' : 'a';
            text[i] = (text[i] - base - shift + 26) % 26 + base;
        }
    }
}

// Main Dispatcher
int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("Usage: tools <mode: wordcount|encrypt|decrypt> <text> [shift]\n");
        return 1;
    }

    char mode[16];
    strncpy(mode, argv[1], 15);
    mode[15] = '\0';

    char text[1024];
    strncpy(text, argv[2], sizeof(text)-1);
    text[sizeof(text)-1] = '\0';

    if (strcmp(mode, "wordcount") == 0) {
        printf("%d\n", wordcount(text));
    } else if (strcmp(mode, "encrypt") == 0) {
        int shift = (argc >= 4) ? atoi(argv[3]) : 3;
        encrypt(text, shift);
        printf("%s\n", text);
    } else if (strcmp(mode, "decrypt") == 0) {
        int shift = (argc >= 4) ? atoi(argv[3]) : 3;
        decrypt(text, shift);
        printf("%s\n", text);
    } else {
        printf("Invalid mode. Use wordcount, encrypt, or decrypt.\n");
        return 1;
    }

    return 0;
}
