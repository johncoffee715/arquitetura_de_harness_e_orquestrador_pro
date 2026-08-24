---
tags:
  - texto
source: "textos, pdf e esquemas"
---

# projeto Controle Analítico termico

- usar um sensor de umidade (DHT22 ou similar) associado a um Arduino para desligar a Peltier (ou reduzir o PWM) caso a temperatura do fluido chegue a 2°C de distância do ponto de orvalho calculado.
-usar um Controlador PID para a Peltier? Isso permitiria manter a água exatamente em, por exemplo, 20°C constantes, independente da carga da GPU.
-Reservatório Chiller (Lado Frio)>>>Bomba 1 e 2>>>GPU e CPU>>>Radiadores>>>Bloco da Face Quente da Peltier>>>Retorno ao Reservatório>>>Loop
-Insertos Metálicos: Não parafuse diretamente na resina. Com o tempo e o calor, a rosca no epóxi vai espanar. Use insertos rosqueados de latão (termofixados ou colados) na carcaça do reservatório. Isso permitirá que você aplique o torque necessário para esmagar a pastilha entre as duas superfícies de cobre sem risco de falha mecânica.
-cura seja total (geralmente 7 dias para dureza máxima) e, se possível, faça um "pós-cura" térmico suave (deixe o reservatório em um local a 40∘C por algumas horas após a cura inicial) para elevar a estabilidade térmica.
-Dica Pro: O cobre é muito liso. Para a resina não "descolar" da chapa com a contração térmica do frio, faça ranhuras mecânicas ou furos na borda da chapa de cobre para que a resina "abrace" o metal mecanicamente, em vez de depender apenas da adesão química.
-Espessura das Paredes: Para aguentar a pressão das bombas de 10m de coluna, não projete paredes menores que 8mm a 10mm. O epóxi cristal é rígido, mas pode ser quebradiço sob estresse pontual.
-após validar que não há vazamentos, você terá que cobrir o reservatório com a espuma elastomérica. Janela de Inspeção: Você pode deixar uma pequena "janela" sem isolamento para ver o fluido, mas lembre-se: essa janela será um ponto de condensação constante.
-Resinas epóxi são resistentes, mas alguns aditivos de Water Cooling (especialmente os coloridos "opaque" ou com etilenoglicol em alta concentração) podem atacar a superfície da resina ao longo de meses, tornando-a opaca ou amarelada.    Recomendação: Use fluido transparente com inibidores de corrosão biológica e galvânica de boa procedência para manter a integridade da resina.
-Limpe o cobre com álcool isopropílico e passe uma lixa grossa na área de contato com a resina para aumentar a área de superfície de adesão química.
-Condensação Interna: Se houver qualquer bolha de ar presa no topo do reservatório, você verá a condensação ocorrer dentro do reservatório antes de ocorrer fora, servindo como um alerta precoce para o seu controle de umidade.
-