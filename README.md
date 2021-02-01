# IqOptionBOT

Bot feito usando a api feita pelo Lu-Yi-Hsun, portanto é necessário clonar o repo dele na mesma pasta desse projeto. (em algum futuro talvez eu adicione como submodule)
```bash
git clone https://github.com/Lu-Yi-Hsun/iqoptionapi
git clone https://github.com/raviston/IqOptionBOT
```
# Modo de uso
O bot ainda não está em sua versão final, se tudo der certo vou adicionando mais funcionalidades e aprimorando seu funcionamento, mas por enquanto na versão 1.0 temos um funcionamento bem simples e intuitivo.

Alguns detalhes que valem a pena ser citados:
* Por segurança a conta vem setada como PRACTICE, se quiser usar o dinheiro real é só marcar a checkbox
* O tempo deve ser fornecido no formato (HH:MM:SS), não coloquei nenhuma verificação anti-animal nessa parte
* Caso você agende uma operação para as 22:30:00 e feche o programa antes desse horário, a operação não será realizada
* O iqOption tem um delay de 2 segundos para começar a realizar a operação, portanto se deseja operar exatamente as 22:30:00, defina o horário para 22:29:58.
* Por enquanto o bot só funciona com as operações binárias. As digitais serão inclusas no futuro

## TESTE ABSOLUTAMENTE QUALQUER OPERAÇÃO NA CONTA PRACTICE ANTES DE USAR A CONTA REAL, O BOT PODE CONTER BUGS NÃO MAPEADOS 