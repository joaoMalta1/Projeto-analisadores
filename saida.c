#include <stdio.h>
#include <string.h>
void ligar(char* d) { printf("%s ligado!\n", d); }
void desligar(char* d) { printf("%s desligado!\n", d); }
void alerta(char* d, char* msg) {
    printf("%s recebeu o alerta:\n", d);
    printf("%s\n", msg);
}
void alerta_com_valor(char* d, char* msg, int val) {
    printf("%s recebeu o alerta:\n", d);
    printf("%s %d\n", msg, val);
}
int main() {
    int monitor = 0;
    int celular = 0;
    int Termometro = 0;
    int temperatura = 0;
    temperatura = 37;
    alerta_com_valor("Termometro", "Temperatura em", temperatura);
    alerta("monitor", "Alerta geral!");
    alerta("celular", "Alerta geral!");
    return 0;
}
