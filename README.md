# Desafio
> O objetivo geral do projeto é coletar dados, transformá-los e armazená-los em diferentes bases de dados e realizar uma análise exploratória de dados (em outras pelavras, extrair conhecimento desses dados) de uma empresa exportadora de produtos.
>
> Você terá acesso a um servidor que transmite dados em JSON (via localhost:3000) com o seguinte template:
> - id: Identificação da transação realizada.
> - time: data da transação (Unix Timestamp).
> - prod_1 – prod_7: quantidade de produtos comprados (em unidades).
> - prod_8 – prod_20: quantidade de produtos comprados (em kg).
>
> Você deve gerar e organizar quatro bases de dados:
> - all_sales.csv – Base de dados com todas as transações realizadas.
> - monthly_sales.csv – Base de dados com o consolidado total de transações dentro de um mês.
> - weekly_price.csv – Base de dados contendo o preço semanal dos produtos, em R$.
> - monthly_revenue.csv – Base de dados contendo o total de vendas mensal, em R$.
>
> A mudança de preço semanal segue a seguinte lógica:
> - Caso o produto seja novo (i.e. primeira semana), você deve fazer a precificação da forma que preferir (e.g. aleatório).
> - Para as semanas seguintes, calcule a média da quantidade de vendas M(t), tanto para a semana anterior quanto para a semana corrente. Em seguida, calcule a variação percentual da quantidade de vendas.
> - O reajuste do preço seguirá a seguinte fórmula:<br>
> 𝑃(𝑡 + 1) = 𝑓(𝑣) * 𝑃(𝑡)<br>
> Sendo 𝑓(𝑣) uma função que define a proporção definida como uma função do tipo logística, definida como:<br>
> 𝑓(𝑣) = 0.5 + 1/(1+𝑒 <sup>−𝑣</sup> )<br>
> E a variação relativa definida como:<br>
> 𝑣 = (𝑀(𝑡)−𝑀(𝑡−1))/𝑀(𝑡−1)<br>
> onde 𝑃(𝑡) é o preço na semana t, e v é a variação da quantidade de vendas.
>
> Sendo assim, as quatro bases deversão ser acessadas por um dashboard que apresenta uma visualização dos dados para análises pertinentes.
# Solução
Para o programa aqui criado como solução ser executado, deve-se primeiramente realizar a configuração do servidor para coleta de dados, bem como do dashboard para visualização. Tal configuração pode ser realizada seguindo as recomendações presentes no repositório [ada_project](https://github.com/mdrs-thiago/ada_project) do professor Thiago Medeiros.<br>
Então, o programa pode ser executado por meio do arquivo ```main.py```. Enquanto o programa estiver sendo executado, cada vez que o usuario pressiona ```Enter```, é realizada uma requisição de novos dados (simulando uma nova semana), além do dashboard ser atualizado.<br>
## Diagrama do programa.
![diagrama](https://user-images.githubusercontent.com/94374033/204178810-d3797f94-7573-4c72-b412-c47dc57d417c.png)
