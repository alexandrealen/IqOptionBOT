# IqOptionBOT
Bot feito usando a api feita pelo Lu-Yi-Hsun, portanto é necessário clonar o repo dele na mesma pasta desse projeto.
```bash
git clone https://github.com/Lu-Yi-Hsun/iqoptionapi
git clone https://github.com/raviston/IqOptionBOT
python main.py
```
# Modo de uso
 versão 1.0 tem um funcionamento bem simples e intuitivo.

Alguns detalhes que valem a pena ser citados:
* Por segurança a conta vem setada como PRACTICE, se quiser usar o dinheiro real é só marcar a checkbox
* O tempo deve ser fornecido no formato (HH:MM:SS), não coloquei nenhuma verificação nessa parte
* Caso você agende uma operação para as 22:30:00 e feche o programa antes desse horário, a operação não será realizada
* O iqOption tem um delay de 2 segundos para começar a realizar a operação, portanto se deseja operar exatamente as 22:30:00, defina o horário para 22:29:58.
