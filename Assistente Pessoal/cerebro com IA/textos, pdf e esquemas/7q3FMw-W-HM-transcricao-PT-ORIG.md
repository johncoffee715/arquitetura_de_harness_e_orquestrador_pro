---
video_id: 7q3FMw-W-HM
titulo: "SQLite 3: O Truque Que Evita Corrupção de Dados? - Fabio Akita"
canal: Dev ao Cubo
duracao: 10:20
url: https://www.youtube.com/watch?v=7q3FMw-W-HM
data_ingestao: 2026-09-17
ingestor: gran-mestre (cloud-direct, quota-fallback)
---

# Transcrição PT-ORIG — bruta (dedupe básico; limpeza profunda pendente)

tem<00:00:05.120><c> um</c><00:00:05.440><c> journal</c><00:00:06.160><c> para</c><00:00:06.399><c> economizar</c><00:00:07.040><c> recursos.</c>
tem um journal para economizar recursos.
Aquele<00:00:07.960><c> comando</c><00:00:08.440><c> replace</c><00:00:08.920><c> que</c><00:00:09.040><c> eu</c><00:00:09.160><c> mostrei</c><00:00:09.440><c> lá</c>
Aquele comando replace que eu mostrei lá
no<00:00:09.800><c> começo</c><00:00:10.080><c> com</c><00:00:10.240><c> DBAS</c><00:00:11.000><c> escreve</c><00:00:11.440><c> por</c><00:00:11.719><c> cima</c><00:00:11.960><c> do</c>
no começo com DBAS escreve por cima do
registro<00:00:12.639><c> antigo</c><00:00:13.000><c> no</c><00:00:13.200><c> arquivo</c><00:00:13.559><c> DBF</c>
registro antigo no arquivo DBF
diretamente.<00:00:14.719><c> Isso</c><00:00:14.920><c> é</c><00:00:15.040><c> péssimo</c><00:00:15.639><c> porque</c>
diretamente. Isso é péssimo porque
digamos<00:00:16.240><c> que</c><00:00:16.440><c> estamos</c><00:00:16.800><c> fazendo</c><00:00:17.080><c> uma</c>
digamos que estamos fazendo uma
atualização<00:00:17.840><c> em</c><00:00:18.080><c> massa</c><00:00:18.600><c> em</c><00:00:18.840><c> todos</c><00:00:19.039><c> os</c>
atualização em massa em todos os
registros<00:00:19.560><c> do</c><00:00:19.680><c> arquivo,</c><00:00:20.039><c> colocando</c><00:00:20.480><c> prefixo</c>
registros do arquivo, colocando prefixo
9<00:00:21.480><c> em</c><00:00:21.680><c> todo</c><00:00:21.840><c> o</c><00:00:21.960><c> telefone</c><00:00:22.439><c> que</c><00:00:22.519><c> é</c><00:00:22.640><c> de</c><00:00:22.760><c> São</c><00:00:22.920><c> Paulo</c>
9 em todo o telefone que é de São Paulo
lá<00:00:23.320><c> em</c><00:00:23.760><c> 2012.</c><00:00:24.279><c> Agora,</c><00:00:24.560><c> digamos</c><00:00:24.920><c> que</c><00:00:25.039><c> no</c><00:00:25.240><c> meio</c>
lá em 2012. Agora, digamos que no meio
dessa<00:00:25.720><c> atualização,</c><00:00:26.560><c> acabou</c><00:00:26.960><c> a</c><00:00:27.080><c> luz</c><00:00:27.439><c> e</c><00:00:27.599><c> o</c>
dessa atualização, acabou a luz e o
computador<00:00:28.240><c> rebuta.</c><00:00:29.160><c> Fodeu.</c><00:00:30.000><c> Isso</c><00:00:30.240><c> era</c><00:00:30.519><c> comum</c>
computador rebuta. Fodeu. Isso era comum
antigamente,<00:00:31.519><c> significava</c><00:00:32.160><c> que</c><00:00:32.399><c> muito</c>
antigamente, significava que muito
provavelmente<00:00:33.520><c> o</c><00:00:33.680><c> arquivo</c><00:00:34.040><c> ficou</c><00:00:34.320><c> num</c><00:00:34.600><c> estado</c>
provavelmente o arquivo ficou num estado
corrompido<00:00:35.640><c> e</c><00:00:35.800><c> eu</c><00:00:35.960><c> perdi</c><00:00:36.280><c> algum</c><00:00:36.559><c> dado.</c><00:00:37.200><c> Hoje</c>
corrompido e eu perdi algum dado. Hoje
em<00:00:37.480><c> dia</c><00:00:37.680><c> não</c><00:00:37.879><c> se</c><00:00:38.000><c> faz</c><00:00:38.280><c> mais</c><00:00:38.480><c> isso.</c><00:00:38.840><c> Existem</c>
em dia não se faz mais isso. Existem
diversas<00:00:39.800><c> estratégias,</c><00:00:40.600><c> mas</c><00:00:40.760><c> o</c><00:00:40.920><c> Colite</c><00:00:41.480><c> 3</c>
diversas estratégias, mas o Colite 3
escolheu<00:00:42.200><c> um</c><00:00:42.399><c> log</c><00:00:42.719><c> de</c><00:00:42.879><c> escrita</c><00:00:43.239><c> pra</c><00:00:43.440><c> frente</c><00:00:43.760><c> ou</c>
escolheu um log de escrita pra frente ou
write<00:00:44.320><c> a</c><00:00:44.520><c> head</c><00:00:44.760><c> log.</c><00:00:45.360><c> Ele</c><00:00:45.520><c> primeiro</c><00:00:45.879><c> escreve</c>
write a head log. Ele primeiro escreve
as<00:00:46.360><c> modificações</c><00:00:46.960><c> nesse</c><00:00:47.280><c> arquivo</c><00:00:47.680><c> separado</c>
as modificações nesse arquivo separado
de<00:00:48.320><c> log.</c><00:00:48.879><c> Depois</c><00:00:49.199><c> que</c><00:00:49.399><c> termina</c><00:00:49.800><c> troca</c><00:00:50.120><c> um</c><00:00:50.320><c> pelo</c>
de log. Depois que termina troca um pelo
outro.<00:00:50.879><c> Bem</c><00:00:51.160><c> simplificado,</c><00:00:52.120><c> é</c><00:00:52.280><c> como</c><00:00:52.440><c> se</c><00:00:52.520><c> eu</c>
outro. Bem simplificado, é como se eu
tivesse<00:00:52.960><c> um</c><00:00:53.120><c> arquivo</c><00:00:53.480><c> chamado</c><00:00:54.000><c> contatos.</c><00:00:54.760><c> Daí</c>
tivesse um arquivo chamado contatos. Daí
eu<00:00:55.039><c> tenho</c><00:00:55.199><c> uma</c><00:00:55.440><c> cópia</c><00:00:55.760><c> dele</c><00:00:56.000><c> chamada</c><00:00:56.480><c> contatos</c>
eu tenho uma cópia dele chamada contatos
wall.<00:00:57.440><c> E</c><00:00:57.600><c> as</c><00:00:57.719><c> atualizações</c><00:00:58.320><c> eu</c><00:00:58.480><c> faço</c><00:00:58.760><c> nesse</c>
wall. E as atualizações eu faço nesse
segundo<00:00:59.399><c> arquivo.</c><00:00:59.800><c> Se</c><00:00:59.920><c> tudo</c><00:01:00.160><c> correu</c><00:01:00.480><c> bem</c><00:01:00.640><c> até</c>
segundo arquivo. Se tudo correu bem até
o<00:01:00.920><c> fim,</c><00:01:01.280><c> agora</c><00:01:01.480><c> eu</c><00:01:01.640><c> troco</c><00:01:01.920><c> um</c><00:01:02.120><c> arquivo</c><00:01:02.519><c> pelo</c>
o fim, agora eu troco um arquivo pelo
outro.<00:01:03.440><c> É</c><00:01:03.600><c> um</c><00:01:03.760><c> pouco</c><00:01:03.960><c> mais</c><00:01:04.239><c> avançado</c><00:01:04.839><c> que</c>
outro. É um pouco mais avançado que
isso,<00:01:05.479><c> mas</c><00:01:05.640><c> só</c><00:01:05.840><c> para</c><00:01:06.000><c> ter</c><00:01:06.159><c> na</c><00:01:06.360><c> cabeça</c><00:01:06.760><c> a</c><00:01:06.960><c> ideia,</c>
isso, mas só para ter na cabeça a ideia,
se<00:01:07.560><c> acabar</c><00:01:07.960><c> a</c><00:01:08.119><c> luz</c><00:01:08.320><c> e</c><00:01:08.479><c> o</c><00:01:08.600><c> segundo</c><00:01:08.920><c> arquivo</c>
se acabar a luz e o segundo arquivo
estragar,<00:01:10.000><c> ainda</c><00:01:10.240><c> tem</c><00:01:10.400><c> o</c><00:01:10.479><c> original</c><00:01:11.040><c> intacto.</c>
estragar, ainda tem o original intacto.
Além<00:01:11.720><c> disso,</c><00:01:12.200><c> se</c><00:01:12.400><c> precisar</c><00:01:12.759><c> fazer</c><00:01:13.080><c> pesquisas,</c>
Além disso, se precisar fazer pesquisas,
eu<00:01:13.799><c> posso</c><00:01:14.040><c> pesquisar</c><00:01:14.520><c> no</c><00:01:14.759><c> original</c><00:01:15.360><c> enquanto</c>
eu posso pesquisar no original enquanto
a<00:01:15.920><c> transação</c><00:01:16.360><c> não</c><00:01:16.560><c> acaba</c><00:01:16.880><c> no</c><00:01:17.080><c> segundo</c>
a transação não acaba no segundo
arquivo,<00:01:17.960><c> em</c><00:01:18.119><c> vez</c><00:01:18.280><c> de</c><00:01:18.439><c> ficar</c><00:01:18.720><c> travado,</c><00:01:19.360><c> tendo</c>
arquivo, em vez de ficar travado, tendo
que<00:01:19.799><c> esperar</c><00:01:20.119><c> até</c><00:01:20.439><c> todas</c><00:01:20.640><c> as</c><00:01:20.799><c> operações</c>
que esperar até todas as operações
acabarem.<00:01:21.960><c> Todo</c><00:01:22.240><c> banco</c><00:01:22.520><c> de</c><00:01:22.680><c> dados</c><00:01:22.960><c> tem</c><00:01:23.119><c> algum</c>
acabarem. Todo banco de dados tem algum
mecanismo<00:01:23.840><c> desse</c><00:01:24.200><c> tipo</c><00:01:24.479><c> mais</c><00:01:24.680><c> sofisticado</c>
mecanismo desse tipo mais sofisticado
para<00:01:25.759><c> ter</c><00:01:25.880><c> o</c><00:01:26.040><c> menor</c><00:01:26.439><c> tempo</c><00:01:26.680><c> de</c><00:01:26.960><c> trava</c><00:01:27.360><c> quanto</c>
para ter o menor tempo de trava quanto
possível<00:01:28.000><c> e</c><00:01:28.159><c> garantir</c><00:01:28.560><c> que</c><00:01:28.720><c> nenhum</c><00:01:29.119><c> dado</c><00:01:29.400><c> vai</c>
possível e garantir que nenhum dado vai
ser<00:01:29.759><c> corrompido.</c><00:01:30.600><c> É</c><00:01:30.720><c> um</c><00:01:30.840><c> tipo</c><00:01:31.040><c> de</c><00:01:31.240><c> mecanismo</c>
ser corrompido. É um tipo de mecanismo
de<00:01:32.040><c> call</c><00:01:32.320><c> ou</c><00:01:32.640><c> copy</c><00:01:33.040><c> ong</c><00:01:33.680><c> como</c><00:01:33.840><c> o</c><00:01:34.000><c> sistema</c><00:01:34.280><c> de</c>
de call ou copy ong como o sistema de
arquivos<00:01:34.920><c> Butter</c><00:01:35.360><c> FS</c><00:01:35.840><c> também</c><00:01:36.159><c> tem</c><00:01:36.399><c> em</c><00:01:36.520><c> Linux.</c>
arquivos Butter FS também tem em Linux.
Por<00:01:37.360><c> isso</c><00:01:37.520><c> que</c><00:01:37.640><c> é</c><00:01:37.799><c> bem</c><00:01:38.200><c> incomum</c><00:01:38.680><c> hoje</c><00:01:38.920><c> em</c><00:01:39.000><c> dia</c>
Por isso que é bem incomum hoje em dia
perder<00:01:39.640><c> dados.</c><00:01:40.119><c> Mesmo</c><00:01:40.520><c> Windows</c><00:01:40.880><c> tem</c><00:01:41.320><c> NTFS</c><00:01:42.320><c> que</c>
perder dados. Mesmo Windows tem NTFS que
protege<00:01:43.040><c> razoavelmente</c><00:01:43.799><c> bem.</c><00:01:44.079><c> Qualquer</c>
protege razoavelmente bem. Qualquer
Linux<00:01:44.840><c> mais</c><00:01:45.079><c> vagabundo</c><00:01:45.840><c> usa</c><00:01:46.079><c> pelo</c><00:01:46.360><c> menos</c><00:01:46.640><c> este</c>
Linux mais vagabundo usa pelo menos este
X<00:01:46.920><c> T4</c><00:01:47.399><c> que</c><00:01:47.560><c> tem</c><00:01:47.759><c> suporte</c><00:01:48.320><c> a</c><00:01:48.479><c> journal.</c><00:01:49.240><c> Para</c>
X T4 que tem suporte a journal. Para
perder<00:01:49.840><c> dados</c><00:01:50.240><c> hoje,</c><00:01:50.560><c> você</c><00:01:50.719><c> precisa</c><00:01:51.000><c> estar</c>
perder dados hoje, você precisa estar
usando<00:01:51.439><c> um</c><00:01:51.680><c> hardware</c><00:01:52.240><c> muito</c><00:01:52.520><c> do</c><00:01:52.719><c> vagabundo,</c>
usando um hardware muito do vagabundo,
como<00:01:53.680><c> um</c><00:01:53.880><c> SD</c><00:01:54.280><c> card</c><00:01:54.560><c> de</c><00:01:54.759><c> câmera.</c><00:01:55.520><c> SD</c><00:01:56.000><c> card</c><00:01:56.399><c> é</c><00:01:56.560><c> um</c>
como um SD card de câmera. SD card é um
hardware<00:01:57.119><c> de</c><00:01:57.280><c> armazenamento</c><00:01:58.200><c> que</c><00:01:58.399><c> foi</c><00:01:58.640><c> feito</c>
hardware de armazenamento que foi feito
para<00:01:59.159><c> ter</c><00:01:59.399><c> grande</c><00:01:59.719><c> capacidade</c><00:02:00.479><c> e</c><00:02:00.640><c> ser</c><00:02:00.880><c> super</c>
para ter grande capacidade e ser super
barato.<00:02:01.640><c> Ele</c><00:02:01.799><c> foi</c><00:02:01.960><c> feito</c><00:02:02.240><c> para</c><00:02:02.439><c> tirar</c><00:02:02.759><c> foto,</c>
barato. Ele foi feito para tirar foto,
gravar<00:02:03.719><c> vídeo,</c><00:02:04.079><c> logo</c><00:02:04.280><c> em</c><00:02:04.399><c> seguida</c><00:02:04.719><c> transferir</c>
gravar vídeo, logo em seguida transferir
para<00:02:05.320><c> um</c><00:02:05.479><c> computador.</c><00:02:06.200><c> Não</c><00:02:06.399><c> foi</c><00:02:06.600><c> feito</c><00:02:06.880><c> para</c>
para um computador. Não foi feito para
deixar<00:02:07.320><c> lá</c><00:02:07.479><c> guardado</c><00:02:07.920><c> para</c><00:02:08.119><c> sempre.</c><00:02:08.679><c> Não</c><00:02:08.800><c> é</c>
deixar lá guardado para sempre. Não é
confiável<00:02:09.679><c> e</c><00:02:09.879><c> podemos</c><00:02:10.239><c> perder</c><00:02:10.560><c> dados</c><00:02:10.920><c> do</c>
confiável e podemos perder dados do
nada,<00:02:11.400><c> especialmente</c><00:02:11.959><c> nos</c><00:02:12.200><c> modelos</c><00:02:12.520><c> mais</c>
nada, especialmente nos modelos mais
baratos.<00:02:13.360><c> SSDs</c><00:02:13.959><c> baratos</c><00:02:14.280><c> de</c><00:02:14.400><c> AliExpress,</c>
baratos. SSDs baratos de AliExpress,
mesma<00:02:15.440><c> coisa,</c><00:02:15.920><c> mas</c><00:02:16.120><c> nesse</c><00:02:16.440><c> caso</c><00:02:16.680><c> porque</c><00:02:16.879><c> são</c>
mesma coisa, mas nesse caso porque são
fraudes<00:02:17.640><c> mesmo,</c><00:02:18.040><c> fabricados</c><00:02:18.640><c> para</c><00:02:18.840><c> falhar.</c>
fraudes mesmo, fabricados para falhar.
Cuidado<00:02:19.640><c> com</c><00:02:19.840><c> isso.</c><00:02:20.440><c> Outra</c><00:02:20.680><c> característica</c>
Cuidado com isso. Outra característica
que<00:02:21.519><c> bancos</c><00:02:21.840><c> relacionais</c><00:02:22.360><c> trouxeram</c><00:02:22.800><c> foi</c>
que bancos relacionais trouxeram foi
esse<00:02:23.120><c> conceito</c><00:02:23.440><c> de</c><00:02:23.599><c> transação</c><00:02:24.200><c> e</c><00:02:24.800><c> de</c>
esse conceito de transação e de
atomicidade<00:02:25.840><c> nas</c><00:02:26.120><c> operações.</c><00:02:26.959><c> Ou</c><00:02:27.160><c> todas</c>
atomicidade nas operações. Ou todas
acabam<00:02:27.920><c> com</c><00:02:28.160><c> sucesso</c><00:02:28.599><c> ou</c><00:02:28.800><c> nenhum</c><00:02:29.200><c> acaba</c><00:02:29.720><c> e</c><00:02:29.920><c> de</c>
acabam com sucesso ou nenhum acaba e de
consistência,<00:02:30.840><c> por</c><00:02:31.040><c> exemplo,</c><00:02:31.400><c> regras</c><00:02:31.720><c> de</c>
consistência, por exemplo, regras de
unicidade,<00:02:32.640><c> chaves</c><00:02:33.040><c> estrangeiras</c><00:02:33.599><c> e</c><00:02:33.760><c> tudo</c>
unicidade, chaves estrangeiras e tudo
mais.<00:02:34.280><c> Os</c><00:02:34.440><c> dados</c><00:02:34.760><c> precisam</c><00:02:35.160><c> sempre</c><00:02:35.480><c> seguir</c>
mais. Os dados precisam sempre seguir
essas<00:02:36.319><c> regras,</c><00:02:36.640><c> sem</c><00:02:36.800><c> exceção.</c><00:02:37.640><c> Isolamento,</c>
essas regras, sem exceção. Isolamento,
ou<00:02:38.640><c> seja,</c><00:02:38.879><c> se</c><00:02:39.040><c> tem</c><00:02:39.159><c> um</c><00:02:39.280><c> conjunto</c><00:02:39.599><c> de</c>
ou seja, se tem um conjunto de
transações<00:02:40.239><c> que</c><00:02:40.360><c> roda</c><00:02:40.599><c> em</c><00:02:40.680><c> paralelo,</c><00:02:41.280><c> o</c>
transações que roda em paralelo, o
resultado<00:02:41.920><c> tem</c><00:02:42.080><c> que</c><00:02:42.200><c> ser</c><00:02:42.360><c> o</c><00:02:42.519><c> mesmo</c><00:02:42.720><c> se</c><00:02:42.840><c> eles</c>
resultado tem que ser o mesmo se eles
tivessem<00:02:43.360><c> rodado</c><00:02:43.720><c> sequencialmente.</c><00:02:44.680><c> O</c><00:02:44.800><c> banco</c>
tivessem rodado sequencialmente. O banco
não<00:02:45.280><c> pode</c><00:02:45.519><c> ficar</c><00:02:45.760><c> num</c><00:02:45.959><c> estado</c><00:02:46.440><c> inconsistente</c>
não pode ficar num estado inconsistente
e<00:02:47.440><c> durabilidade</c><00:02:48.360><c> que</c><00:02:48.519><c> se</c><00:02:48.640><c> a</c><00:02:48.800><c> transação</c><00:02:49.360><c> diz</c>
e durabilidade que se a transação diz
que<00:02:50.120><c> gravou</c><00:02:50.480><c> o</c><00:02:50.599><c> dado,</c><00:02:51.080><c> podemos</c><00:02:51.400><c> acreditar</c><00:02:51.920><c> que</c>
que gravou o dado, podemos acreditar que
realmente<00:02:52.599><c> tá</c><00:02:52.800><c> fisicamente</c><00:02:53.440><c> no</c><00:02:53.680><c> disco.</c><00:02:54.239><c> Caso</c>
realmente tá fisicamente no disco. Caso
um<00:02:54.599><c> erro</c><00:02:54.840><c> aconteça,</c><00:02:55.319><c> com</c><00:02:55.440><c> uma</c><00:02:55.599><c> famosa</c><00:02:55.959><c> falta</c>
um erro aconteça, com uma famosa falta
de<00:02:56.400><c> luz,</c><00:02:56.680><c> o</c><00:02:56.800><c> banco</c><00:02:57.120><c> precisa</c><00:02:57.480><c> voltar</c><00:02:57.800><c> pro</c>
de luz, o banco precisa voltar pro
último<00:02:58.360><c> estado</c><00:02:58.720><c> consistente</c><00:02:59.360><c> conhecido.</c>
último estado consistente conhecido.
Nunca<00:03:00.560><c> pode</c><00:03:00.920><c> continuar</c><00:03:01.400><c> operando</c><00:03:01.879><c> no</c><00:03:02.040><c> estado</c>
Nunca pode continuar operando no estado
inconsistente.<00:03:03.360><c> Cada</c><00:03:03.640><c> banco</c><00:03:04.200><c> implementa</c>
inconsistente. Cada banco implementa
isso<00:03:04.840><c> de</c><00:03:05.000><c> formas</c><00:03:05.319><c> diferentes,</c><00:03:05.799><c> mas</c><00:03:05.959><c> no</c><00:03:06.159><c> geral</c>
isso de formas diferentes, mas no geral
significa<00:03:07.159><c> que</c><00:03:07.360><c> podemos</c><00:03:07.840><c> confiar</c><00:03:08.239><c> nos</c><00:03:08.519><c> dados</c>
significa que podemos confiar nos dados
num<00:03:09.040><c> banco</c><00:03:09.280><c> de</c><00:03:09.400><c> dados</c><00:03:09.720><c> relacional,</c><00:03:10.400><c> sejam</c>
num banco de dados relacional, sejam
mais<00:03:11.159><c> sequel</c><00:03:11.560><c> ou</c><00:03:11.879><c> postg</c><00:03:12.360><c> ou</c><00:03:12.599><c> sequel</c><00:03:13.000><c> server.</c>
mais sequel ou postg ou sequel server.
No<00:03:13.720><c> geral</c><00:03:14.040><c> eles</c><00:03:14.280><c> implementam</c><00:03:14.799><c> bem</c><00:03:14.959><c> essas</c>
No geral eles implementam bem essas
características.<00:03:16.200><c> mesmo</c><00:03:16.519><c> o</c><00:03:16.599><c> pequeno</c><00:03:16.959><c> Colite</c>
características. mesmo o pequeno Colite
3<00:03:17.879><c> faz</c><00:03:18.120><c> isso.</c><00:03:18.680><c> Um</c><00:03:18.760><c> dos</c><00:03:18.959><c> jeitos</c><00:03:19.239><c> mais</c><00:03:19.519><c> toscos</c><00:03:19.879><c> é</c>
3 faz isso. Um dos jeitos mais toscos é
simplesmente<00:03:20.560><c> bloquear</c><00:03:21.080><c> o</c><00:03:21.239><c> arquivo</c><00:03:21.640><c> todo</c>
simplesmente bloquear o arquivo todo
para<00:03:22.360><c> cada</c><00:03:22.680><c> operação,</c><00:03:23.239><c> esperar</c><00:03:23.640><c> completar</c>
para cada operação, esperar completar
com<00:03:24.159><c> sucesso</c><00:03:24.599><c> e</c><00:03:24.799><c> só</c><00:03:24.920><c> aí</c><00:03:25.159><c> liberar</c><00:03:25.560><c> para</c><00:03:25.720><c> outras</c>
com sucesso e só aí liberar para outras
operações.<00:03:26.599><c> Mas</c><00:03:26.720><c> claro,</c><00:03:27.239><c> isso</c><00:03:27.480><c> seria</c>
operações. Mas claro, isso seria
altamente<00:03:28.439><c> ineficiente.</c><00:03:29.560><c> Mas</c><00:03:29.799><c> era</c><00:03:30.040><c> assim</c><00:03:30.319><c> que</c>
altamente ineficiente. Mas era assim que
bancos<00:03:30.840><c> de</c><00:03:31.000><c> dados</c><00:03:31.599><c> XBASE,</c><00:03:32.280><c> DBF</c><00:03:32.920><c> funcionavam</c>
bancos de dados XBASE, DBF funcionavam
em<00:03:33.760><c> rede</c><00:03:33.959><c> nos</c><00:03:34.200><c> anos</c><00:03:34.480><c> 90,</c><00:03:35.080><c> quando</c><00:03:35.360><c> começamos</c><00:03:35.840><c> a</c>
em rede nos anos 90, quando começamos a
usar<00:03:36.280><c> placas</c><00:03:36.640><c> de</c><00:03:36.799><c> rede</c><00:03:37.080><c> em</c><00:03:37.319><c> MSOs</c><00:03:38.080><c> e</c><00:03:38.280><c> fazer</c>
usar placas de rede em MSOs e fazer
pequenas<00:03:39.000><c> redes</c><00:03:39.280><c> usando</c><00:03:39.599><c> ferramentas</c><00:03:40.080><c> da</c>
pequenas redes usando ferramentas da
antiga<00:03:40.640><c> novel</c><00:03:41.200><c> ou</c><00:03:41.439><c> Windows.</c><00:03:42.519><c> Forework</c><00:03:43.080><c> Groups</c>
antiga novel ou Windows. Forework Groups
ou<00:03:43.680><c> Venerado</c><00:03:44.360><c> S2</c><00:03:44.760><c> da</c><00:03:44.920><c> IBM.</c><00:03:45.640><c> Na</c><00:03:45.799><c> prática,</c><00:03:46.200><c> um</c>
ou Venerado S2 da IBM. Na prática, um
computador<00:03:47.360><c> era</c><00:03:47.599><c> elegido</c><00:03:48.080><c> como</c><00:03:48.239><c> um</c><00:03:48.400><c> servidor</c>
computador era elegido como um servidor
de<00:03:48.959><c> arquivos</c><00:03:49.400><c> e</c><00:03:49.560><c> esses</c><00:03:49.799><c> arquivos</c><00:03:50.280><c> DBF</c><00:03:50.799><c> e</c><00:03:50.920><c> ndX</c>
de arquivos e esses arquivos DBF e ndX
eram<00:03:52.040><c> compartilhados</c><00:03:52.799><c> em</c><00:03:53.040><c> rede</c><00:03:53.519><c> e</c><00:03:53.760><c> todos</c><00:03:54.000><c> os</c>
eram compartilhados em rede e todos os
outros<00:03:54.480><c> computadores</c><00:03:55.079><c> na</c><00:03:55.280><c> rede</c><00:03:55.560><c> enxergavam</c>
outros computadores na rede enxergavam
os<00:03:56.360><c> mesmos</c><00:03:56.720><c> arquivos.</c><00:03:57.519><c> Cada</c><00:03:57.799><c> computador</c>
os mesmos arquivos. Cada computador
tinha<00:03:58.680><c> a</c><00:03:58.879><c> mesma</c><00:03:59.200><c> versão</c><00:03:59.519><c> do</c><00:03:59.760><c> programa</c><00:04:00.159><c> em</c><00:04:00.319><c> the</c>
tinha a mesma versão do programa em the
base<00:04:00.760><c> ou</c><00:04:01.000><c> Clipper</c><00:04:01.400><c> ou</c><00:04:01.599><c> Fox</c><00:04:02.000><c> Pro</c><00:04:02.280><c> instalado.</c><00:04:03.079><c> Se</c>
base ou Clipper ou Fox Pro instalado. Se
algum<00:04:03.480><c> tivesse</c><00:04:03.799><c> uma</c><00:04:04.000><c> versão</c><00:04:04.280><c> mais</c><00:04:04.560><c> antiga</c><00:04:05.000><c> era</c>
algum tivesse uma versão mais antiga era
caos.<00:04:05.879><c> A</c><00:04:06.040><c> consistência,</c><00:04:06.920><c> as</c><00:04:07.200><c> regras</c>
caos. A consistência, as regras
dependiam<00:04:08.400><c> totalmente</c><00:04:08.879><c> da</c><00:04:09.120><c> versão</c><00:04:09.480><c> do</c>
dependiam totalmente da versão do
programa<00:04:10.200><c> instalado</c><00:04:10.599><c> em</c><00:04:10.760><c> cada</c><00:04:11.040><c> máquina.</c><00:04:11.640><c> A</c>
programa instalado em cada máquina. A
atomicidade<00:04:12.879><c> era</c><00:04:13.159><c> mais</c><00:04:13.360><c> ou</c><00:04:13.519><c> menos</c><00:04:13.760><c> garantida</c>
atomicidade era mais ou menos garantida
por<00:04:14.400><c> um</c><00:04:14.519><c> sistema</c><00:04:14.799><c> de</c><00:04:15.079><c> lock.</c><00:04:15.640><c> Quando</c><00:04:15.840><c> um</c>
por um sistema de lock. Quando um
programa<00:04:16.400><c> quisesse</c><00:04:16.799><c> inserir</c><00:04:17.120><c> um</c><00:04:17.239><c> registro</c>
programa quisesse inserir um registro
novo,<00:04:17.919><c> ele</c><00:04:18.199><c> travava</c><00:04:18.759><c> o</c><00:04:18.959><c> acesso</c><00:04:19.280><c> à</c><00:04:19.400><c> aquele</c>
novo, ele travava o acesso à aquele
arquivo.<00:04:20.160><c> Se</c><00:04:20.239><c> um</c><00:04:20.400><c> segundo</c><00:04:20.759><c> computador</c>
arquivo. Se um segundo computador
tentasse<00:04:21.759><c> ler,</c><00:04:22.120><c> recebia</c><00:04:22.600><c> um</c><00:04:22.759><c> erro</c><00:04:23.120><c> que</c><00:04:23.280><c> o</c>
tentasse ler, recebia um erro que o
arquivo<00:04:23.720><c> tava</c><00:04:23.919><c> ocupado</c><00:04:24.320><c> e</c><00:04:24.479><c> precisava</c>
arquivo tava ocupado e precisava
esperar.<00:04:25.639><c> Isso</c><00:04:25.840><c> nem</c><00:04:26.080><c> sempre</c><00:04:26.400><c> funcionava.</c><00:04:27.120><c> E</c>
esperar. Isso nem sempre funcionava. E
se<00:04:27.320><c> o</c><00:04:27.400><c> arquivo</c><00:04:27.759><c> DBF</c><00:04:28.440><c> sozinho</c><00:04:28.919><c> numa</c><00:04:29.199><c> única</c>
se o arquivo DBF sozinho numa única
máquina<00:04:29.960><c> tendia</c><00:04:30.280><c> a</c><00:04:30.360><c> se</c><00:04:30.479><c> corromper</c><00:04:31.199><c> porque</c><00:04:31.400><c> não</c>
máquina tendia a se corromper porque não
existia<00:04:31.800><c> nenhum</c><00:04:32.120><c> sistema</c><00:04:32.400><c> de</c><00:04:32.560><c> proteção</c><00:04:33.039><c> como</c>
existia nenhum sistema de proteção como
Journals.<00:04:34.080><c> Imagine</c><00:04:34.479><c> em</c><00:04:34.680><c> rede</c><00:04:35.199><c> corromper</c>
Journals. Imagine em rede corromper
arquivos<00:04:36.160><c> era</c><00:04:36.440><c> rotina.</c><00:04:37.199><c> Experimenta</c>
arquivos era rotina. Experimenta
esquecer<00:04:37.960><c> de</c><00:04:38.080><c> fazer</c><00:04:38.280><c> backup</c><00:04:38.680><c> no</c><00:04:38.840><c> fim</c><00:04:39.000><c> do</c><00:04:39.120><c> dia.</c>
esquecer de fazer backup no fim do dia.
Certeza<00:04:40.039><c> que</c><00:04:40.199><c> no</c><00:04:40.360><c> dia</c><00:04:40.560><c> seguinte</c><00:04:41.000><c> ia</c><00:04:41.039><c> dar</c><00:04:41.199><c> pau</c><00:04:41.560><c> e</c>
Certeza que no dia seguinte ia dar pau e
corromper<00:04:42.160><c> alguma</c><00:04:42.479><c> coisa.</c><00:04:42.800><c> Sistemas</c><00:04:43.160><c> de</c>
corromper alguma coisa. Sistemas de
arquivos<00:04:43.639><c> em</c><00:04:43.759><c> rede</c><00:04:44.000><c> como</c><00:04:44.240><c> novel</c><00:04:44.800><c> era</c><00:04:45.000><c> uma</c>
arquivos em rede como novel era uma
gambiarra<00:04:46.440><c> feita</c><00:04:46.840><c> em</c><00:04:47.039><c> cima</c><00:04:47.280><c> do</c><00:04:47.479><c> DOS</c><00:04:47.919><c> com</c>
gambiarra feita em cima do DOS com
tecnologias<00:04:49.000><c> super</c><00:04:49.440><c> imaturas.</c><00:04:50.520><c> Hoje</c><00:04:50.759><c> usamos</c>
tecnologias super imaturas. Hoje usamos
protocolos<00:04:51.800><c> de</c><00:04:52.039><c> internet</c><00:04:52.600><c> como</c><00:04:52.840><c> TCP,</c><00:04:53.360><c> IP,</c><00:04:53.800><c> mas</c>
protocolos de internet como TCP, IP, mas
naquela<00:04:54.320><c> época</c><00:04:54.759><c> usávamos</c><00:04:55.360><c> protocolos</c><00:04:55.880><c> mais</c>
naquela época usávamos protocolos mais
rudimentares<00:04:56.960><c> como</c><00:04:57.280><c> IPX,</c><00:04:57.880><c> SPX</c><00:04:58.400><c> e</c><00:04:58.600><c> Netbills</c><00:04:59.160><c> da</c>
rudimentares como IPX, SPX e Netbills da
Microsoft.<00:05:00.320><c> Verdadeiras</c><00:05:01.000><c> porcarias.</c><00:05:01.880><c> E</c>
Microsoft. Verdadeiras porcarias. E
mesmo<00:05:02.199><c> a</c><00:05:02.320><c> tecnologia</c><00:05:02.840><c> de</c><00:05:03.039><c> redes</c><00:05:03.320><c> em</c><00:05:03.479><c> si.</c><00:05:03.960><c> Hoje</c>
mesmo a tecnologia de redes em si. Hoje
usamos<00:05:04.560><c> Ethernet</c><00:05:05.199><c> 1</c><00:05:05.280><c> GB</c><00:05:05.759><c> para</c><00:05:05.919><c> cima.</c>
usamos Ethernet 1 GB para cima.
Antigamente<00:05:07.039><c> eram</c><00:05:07.320><c> cabos</c><00:05:07.720><c> coaxiais</c><00:05:08.400><c> que</c><00:05:08.600><c> nem</c>
Antigamente eram cabos coaxiais que nem
de<00:05:08.919><c> TV</c><00:05:09.160><c> a</c><00:05:09.360><c> cabo</c><00:05:09.600><c> que</c><00:05:09.880><c> male</c><00:05:10.240><c> male</c><00:05:10.720><c> faziam</c><00:05:11.120><c> 10</c><00:05:11.400><c> MB,</c>
de TV a cabo que male male faziam 10 MB,
perdiam<00:05:12.639><c> pacotes,</c><00:05:13.199><c> corrompiam</c><00:05:13.840><c> dados</c><00:05:14.160><c> e</c>
perdiam pacotes, corrompiam dados e
assim<00:05:14.560><c> vai.</c><00:05:15.320><c> Com</c><00:05:15.479><c> a</c><00:05:15.600><c> migração</c><00:05:16.000><c> de</c><00:05:16.199><c> MS</c><00:05:16.560><c> Do</c><00:05:16.880><c> para</c>
assim vai. Com a migração de MS Do para
Windows<00:05:17.400><c> e</c><00:05:17.520><c> da</c><00:05:17.639><c> arquitetura</c><00:05:18.120><c> de</c><00:05:18.360><c> 16</c><00:05:18.880><c> bits</c><00:05:19.160><c> para</c>
Windows e da arquitetura de 16 bits para
32<00:05:19.840><c> bits,</c><00:05:20.280><c> ganhamos</c><00:05:20.639><c> até</c><00:05:20.919><c> 4</c><00:05:21.240><c> GB</c><00:05:21.880><c> de</c><00:05:22.039><c> RAM</c><00:05:22.280><c> para</c>
32 bits, ganhamos até 4 GB de RAM para
trabalhar,<00:05:23.080><c> sem</c><00:05:23.319><c> precisar</c><00:05:23.680><c> fazer</c><00:05:23.919><c> gambiarras</c>
trabalhar, sem precisar fazer gambiarras
de<00:05:24.680><c> memória</c><00:05:25.080><c> em</c><00:05:25.199><c> DOS,</c><00:05:25.680><c> como</c><00:05:25.880><c> eu</c><00:05:26.080><c> explico</c><00:05:26.440><c> no</c>
de memória em DOS, como eu explico no
episódio<00:05:27.080><c> dos</c><00:05:27.280><c> 640</c><00:05:28.080><c> KB.</c><00:05:28.720><c> E</c><00:05:28.840><c> com</c><00:05:29.000><c> isso,</c><00:05:29.479><c> em</c><00:05:29.639><c> vez</c>
episódio dos 640 KB. E com isso, em vez
de<00:05:30.080><c> cada</c><00:05:30.360><c> programa,</c><00:05:30.759><c> em</c><00:05:30.960><c> cada</c><00:05:31.160><c> máquina</c><00:05:31.479><c> da</c>
de cada programa, em cada máquina da
rede<00:05:31.880><c> tentar</c><00:05:32.160><c> acessar</c><00:05:32.520><c> diretamente</c><00:05:33.000><c> os</c>
rede tentar acessar diretamente os
arquivos<00:05:33.440><c> de</c><00:05:33.560><c> dados,</c><00:05:34.039><c> eles</c><00:05:34.319><c> passaram</c><00:05:34.639><c> a</c>
arquivos de dados, eles passaram a
conversar<00:05:35.160><c> com</c><00:05:35.319><c> o</c><00:05:35.440><c> software</c><00:05:35.919><c> servidor.</c><00:05:36.639><c> Dessa</c>
conversar com o software servidor. Dessa
forma,<00:05:37.360><c> só</c><00:05:37.600><c> um</c><00:05:37.880><c> software</c><00:05:38.440><c> tinha</c><00:05:38.759><c> acesso</c>
forma, só um software tinha acesso
direto<00:05:39.479><c> aos</c><00:05:39.720><c> arquivos</c><00:05:40.240><c> e</c><00:05:40.479><c> todos</c><00:05:40.720><c> os</c><00:05:40.919><c> outros</c>
direto aos arquivos e todos os outros
programas<00:05:41.720><c> clientes</c><00:05:42.199><c> conversavam</c><00:05:42.880><c> com</c><00:05:43.120><c> esse</c>
programas clientes conversavam com esse
servidor<00:05:44.080><c> usando</c><00:05:44.479><c> algum</c><00:05:44.840><c> protocolo</c><00:05:45.440><c> com</c>
servidor usando algum protocolo com
alguma<00:05:46.120><c> linguagem,</c><00:05:46.840><c> no</c><00:05:47.080><c> caso</c><00:05:47.400><c> o</c><00:05:47.639><c> SQL.</c><00:05:48.479><c> Essa</c>
alguma linguagem, no caso o SQL. Essa
foi<00:05:48.880><c> a</c><00:05:49.039><c> era</c><00:05:49.240><c> de</c><00:05:49.479><c> programas</c><00:05:49.880><c> feitos</c><00:05:50.160><c> em</c><00:05:50.319><c> Visual</c>
foi a era de programas feitos em Visual
Basic<00:05:51.319><c> ou</c><00:05:51.600><c> Del,</c><00:05:52.280><c> conversando</c><00:05:52.880><c> com</c><00:05:53.080><c> bancos</c><00:05:53.400><c> de</c>
Basic ou Del, conversando com bancos de
dados,<00:05:53.919><c> servidores</c><00:05:54.479><c> mais</c><00:05:54.720><c> modernos</c><00:05:55.199><c> como</c>
dados, servidores mais modernos como
Sequel<00:05:55.960><c> Server,</c><00:05:56.319><c> que</c><00:05:56.440><c> tinha</c><00:05:56.680><c> TSQL,</c><00:05:57.520><c> ou</c>
Sequel Server, que tinha TSQL, ou
Oracle,<00:05:58.319><c> que</c><00:05:58.479><c> tinha</c><00:05:58.759><c> PLSQL,</c><00:05:59.759><c> ou</c><00:06:00.000><c> alguns</c><00:06:00.440><c> mais</c>
Oracle, que tinha PLSQL, ou alguns mais
de<00:06:00.840><c> nicho,</c><00:06:01.199><c> como</c><00:06:01.400><c> o</c><00:06:01.560><c> Interbase</c><00:06:02.120><c> da</c><00:06:02.360><c> Borland,</c>
de nicho, como o Interbase da Borland,
que<00:06:03.120><c> era</c><00:06:03.240><c> o</c><00:06:03.360><c> padrão</c><00:06:03.680><c> para</c><00:06:03.840><c> quem</c><00:06:04.039><c> usava</c><00:06:04.440><c> Delph.</c>
que era o padrão para quem usava Delph.
Em<00:06:05.160><c> vez</c><00:06:05.319><c> de</c><00:06:05.520><c> cada</c><00:06:05.880><c> programa</c><00:06:06.319><c> cliente</c><00:06:06.680><c> ter</c><00:06:06.840><c> que</c>
Em vez de cada programa cliente ter que
controlar<00:06:07.400><c> a</c><00:06:07.520><c> integridade</c><00:06:08.120><c> dos</c><00:06:08.319><c> arquivos,</c>
controlar a integridade dos arquivos,
melhor<00:06:09.400><c> terceirizar</c><00:06:10.039><c> isso</c><00:06:10.280><c> para</c><00:06:10.440><c> um</c>
melhor terceirizar isso para um
servidor.<00:06:11.240><c> Os</c><00:06:11.440><c> clientes</c><00:06:11.800><c> só</c><00:06:12.000><c> falam:</c><00:06:12.479><c> "Ô,</c>
servidor. Os clientes só falam: "Ô,
grava<00:06:13.080><c> isso</c><00:06:13.240><c> para</c><00:06:13.400><c> mim"</c><00:06:13.800><c> ou:</c><00:06:14.240><c> "Ô,</c><00:06:14.599><c> pesquisa</c>
grava isso para mim" ou: "Ô, pesquisa
isso<00:06:15.199><c> para</c><00:06:15.319><c> mim".</c><00:06:15.680><c> E</c><00:06:15.759><c> o</c><00:06:15.880><c> servidor</c><00:06:16.240><c> se</c><00:06:16.440><c> vira.</c>
isso para mim". E o servidor se vira.
Isso<00:06:16.960><c> aumentou</c><00:06:17.400><c> muito,</c><00:06:17.720><c> não</c><00:06:17.880><c> só</c><00:06:18.039><c> a</c>
Isso aumentou muito, não só a
escalabilidade,<00:06:18.960><c> mas</c><00:06:19.160><c> também</c><00:06:19.400><c> a</c>
escalabilidade, mas também a
estabilidade.<00:06:20.759><c> Se</c><00:06:20.880><c> um</c><00:06:21.000><c> cliente</c><00:06:21.319><c> manda</c><00:06:21.560><c> uma</c>
estabilidade. Se um cliente manda uma
operação<00:06:22.080><c> não</c><00:06:22.360><c> suportada,</c><00:06:23.080><c> o</c><00:06:23.280><c> servidor</c><00:06:23.680><c> pode</c>
operação não suportada, o servidor pode
só<00:06:24.199><c> recusar</c><00:06:24.800><c> em</c><00:06:24.960><c> vez</c><00:06:25.080><c> de</c><00:06:25.240><c> tentar</c><00:06:25.560><c> executar</c><00:06:26.039><c> e</c>
só recusar em vez de tentar executar e
corromper<00:06:26.639><c> arquivos.</c><00:06:27.520><c> Se</c><00:06:27.680><c> Colet</c><00:06:28.160><c> 3</c>
corromper arquivos. Se Colet 3
oficialmente<00:06:29.000><c> não</c><00:06:29.199><c> tem</c><00:06:29.360><c> um</c><00:06:29.520><c> servidor,</c><00:06:30.240><c> mas</c>
oficialmente não tem um servidor, mas
tem<00:06:30.599><c> gente</c><00:06:30.840><c> tentando</c><00:06:31.240><c> fazer</c><00:06:31.479><c> um</c><00:06:31.639><c> sei</c><00:06:31.800><c> lá</c><00:06:32.000><c> por</c>
tem gente tentando fazer um sei lá por
tem<00:06:32.599><c> um</c><00:06:32.720><c> projeto</c><00:06:33.039><c> chamado</c><00:06:33.400><c> Valentina</c><00:06:33.960><c> DB</c><00:06:34.240><c> que</c>
tem um projeto chamado Valentina DB que
faz<00:06:34.639><c> isso.</c><00:06:35.120><c> Eu</c><00:06:35.160><c> não</c><00:06:35.280><c> vejo</c><00:06:35.479><c> nenhuma</c><00:06:35.919><c> vantagem.</c>
faz isso. Eu não vejo nenhuma vantagem.
Se<00:06:36.599><c> você</c><00:06:36.720><c> quer</c><00:06:36.919><c> um</c><00:06:37.039><c> banco</c><00:06:37.319><c> de</c><00:06:37.479><c> dados</c><00:06:37.880><c> SQL,</c>
Se você quer um banco de dados SQL,
formato<00:06:38.840><c> cliente</c><00:06:39.240><c> servidor,</c><00:06:39.960><c> use</c><00:06:40.280><c> um</c><00:06:40.479><c> de</c>
formato cliente servidor, use um de
verdade<00:06:41.120><c> que</c><00:06:41.280><c> é</c><00:06:41.400><c> maduro,</c><00:06:41.800><c> como</c><00:06:42.039><c> My</c><00:06:42.360><c> Sequel</c><00:06:42.759><c> ou</c>
verdade que é maduro, como My Sequel ou
Postgres.<00:06:43.840><c> Use</c><00:06:44.160><c> Secol</c><00:06:44.319><c> Colet</c><00:06:44.759><c> 3</c><00:06:44.960><c> para</c>
Postgres. Use Secol Colet 3 para
programas<00:06:45.560><c> que</c><00:06:45.800><c> precisam</c><00:06:46.440><c> de</c><00:06:46.639><c> dados</c>
programas que precisam de dados
localmente,<00:06:47.840><c> como</c><00:06:48.039><c> seu</c><00:06:48.240><c> roteador</c><00:06:48.639><c> de</c>
localmente, como seu roteador de
internet,<00:06:49.520><c> relógio,</c><00:06:49.919><c> que</c><00:06:50.039><c> eu</c><00:06:50.120><c> já</c><00:06:50.199><c> dei</c><00:06:50.360><c> de</c>
internet, relógio, que eu já dei de
exemplo.<00:06:51.240><c> Quando</c><00:06:51.520><c> temos</c><00:06:51.800><c> o</c><00:06:52.000><c> formato</c><00:06:52.400><c> de</c><00:06:52.560><c> um</c>
exemplo. Quando temos o formato de um
servidor,<00:06:53.479><c> temos</c><00:06:53.759><c> algumas</c><00:06:54.160><c> vantagens</c><00:06:54.680><c> e</c>
servidor, temos algumas vantagens e
algumas<00:06:55.199><c> desvantagens.</c><00:06:55.960><c> A</c><00:06:56.080><c> primeira</c><00:06:56.479><c> é</c><00:06:56.639><c> que</c><00:06:56.720><c> a</c>
algumas desvantagens. A primeira é que a
velocidade<00:06:57.440><c> vai</c><00:06:57.680><c> depender</c><00:06:58.000><c> da</c><00:06:58.199><c> qualidade</c><00:06:58.759><c> da</c>
velocidade vai depender da qualidade da
rede.<00:06:59.560><c> Tudo</c><00:06:59.800><c> que</c><00:07:00.000><c> roda</c><00:07:00.400><c> localmente</c><00:07:01.160><c> sempre</c><00:07:01.400><c> é</c>
rede. Tudo que roda localmente sempre é
mais<00:07:01.800><c> rápido.</c><00:07:02.319><c> Em</c><00:07:02.520><c> rede</c><00:07:02.800><c> você</c><00:07:03.000><c> precisa</c><00:07:03.240><c> pegar</c>
mais rápido. Em rede você precisa pegar
o<00:07:03.639><c> resultado,</c><00:07:04.319><c> quebrar</c><00:07:04.720><c> em</c><00:07:04.879><c> pacotes,</c><00:07:05.639><c> rotear</c>
o resultado, quebrar em pacotes, rotear
esses<00:07:06.479><c> pacotes,</c><00:07:07.240><c> ir</c><00:07:07.520><c> recebendo,</c><00:07:08.240><c> processando</c>
esses pacotes, ir recebendo, processando
um<00:07:09.000><c> buffer</c><00:07:09.520><c> e</c><00:07:09.720><c> só</c><00:07:09.919><c> aí</c><00:07:10.120><c> vai</c><00:07:10.319><c> ter</c><00:07:10.440><c> os</c><00:07:10.599><c> dados.</c>
um buffer e só aí vai ter os dados.
Podemos<00:07:11.759><c> escolher</c><00:07:12.280><c> ir</c><00:07:12.440><c> recebendo</c><00:07:12.919><c> e</c><00:07:13.120><c> já</c>
Podemos escolher ir recebendo e já
processando<00:07:13.800><c> os</c><00:07:13.919><c> dados</c><00:07:14.240><c> localmente</c><00:07:14.960><c> ou</c>
processando os dados localmente ou
podemos<00:07:15.599><c> escolher</c><00:07:16.120><c> esperar</c><00:07:16.599><c> receber</c><00:07:16.879><c> a</c>
podemos escolher esperar receber a
resposta<00:07:17.599><c> toda</c><00:07:18.000><c> e</c><00:07:18.160><c> só</c><00:07:18.319><c> depois</c><00:07:18.720><c> fazer</c><00:07:18.960><c> alguma</c>
resposta toda e só depois fazer alguma
coisa.<00:07:19.599><c> É</c><00:07:19.720><c> a</c><00:07:19.879><c> diferença</c><00:07:20.160><c> de</c><00:07:20.360><c> receber</c><00:07:20.720><c> tudo</c><00:07:20.960><c> de</c>
coisa. É a diferença de receber tudo de
uma<00:07:21.280><c> vez</c><00:07:21.680><c> ou</c><00:07:21.919><c> usar</c><00:07:22.240><c> técnicas</c><00:07:22.720><c> de</c><00:07:23.000><c> streaming.</c><00:07:23.680><c> E</c>
uma vez ou usar técnicas de streaming. E
aí<00:07:24.039><c> depende</c><00:07:24.360><c> da</c><00:07:24.520><c> sua</c><00:07:24.720><c> pesquisa.</c><00:07:25.319><c> Se</c><00:07:25.440><c> for</c><00:07:25.639><c> tosca</c>
aí depende da sua pesquisa. Se for tosca
e<00:07:26.120><c> mal</c><00:07:26.319><c> feita</c><00:07:26.599><c> e</c><00:07:26.720><c> mandar</c><00:07:26.960><c> tipo</c><00:07:27.160><c> um</c><00:07:27.360><c> select</c>
e mal feita e mandar tipo um select
asterisco<00:07:28.479><c> para</c><00:07:28.599><c> uma</c><00:07:28.759><c> tabela</c><00:07:29.039><c> de</c><00:07:29.240><c> 10</c><00:07:29.520><c> GB</c><00:07:30.120><c> sem</c>
asterisco para uma tabela de 10 GB sem
usar<00:07:30.680><c> stream,</c><00:07:31.360><c> boa</c><00:07:31.680><c> sorte,</c><00:07:32.039><c> vai</c><00:07:32.199><c> ocupar</c><00:07:32.599><c> toda</c>
usar stream, boa sorte, vai ocupar toda
a<00:07:32.919><c> memória</c><00:07:33.280><c> da</c><00:07:33.440><c> sua</c><00:07:33.599><c> máquina</c><00:07:33.879><c> e</c><00:07:34.039><c> mais</c><00:07:34.240><c> o</c><00:07:34.360><c> swap</c>
a memória da sua máquina e mais o swap
em<00:07:34.879><c> disco.</c><00:07:35.599><c> Isso</c><00:07:35.800><c> é</c><00:07:35.919><c> o</c><00:07:36.000><c> que</c><00:07:36.160><c> iniciantes</c><00:07:36.720><c> têm</c>
em disco. Isso é o que iniciantes têm
mais<00:07:37.199><c> dificuldade</c><00:07:37.759><c> de</c><00:07:37.960><c> entender.</c><00:07:38.639><c> Os</c><00:07:38.879><c> dados</c>
mais dificuldade de entender. Os dados
que<00:07:39.560><c> pedem</c><00:07:39.960><c> precisam</c><00:07:40.360><c> ir</c><00:07:40.520><c> para</c><00:07:40.680><c> algum</c><00:07:41.000><c> lugar.</c>
que pedem precisam ir para algum lugar.
Nada<00:07:41.919><c> é</c><00:07:42.039><c> de</c><00:07:42.240><c> graça</c><00:07:42.479><c> em</c><00:07:42.680><c> computação.</c><00:07:43.440><c> O</c>
Nada é de graça em computação. O
trabalho<00:07:44.080><c> principal</c><00:07:44.520><c> de</c><00:07:44.720><c> um</c><00:07:44.840><c> programador</c><00:07:45.400><c> é</c>
trabalho principal de um programador é
justamente<00:07:46.560><c> administrar</c><00:07:47.280><c> os</c><00:07:47.520><c> recursos</c><00:07:48.000><c> da</c>
justamente administrar os recursos da
máquina<00:07:48.479><c> da</c><00:07:48.680><c> maneira</c><00:07:48.960><c> mais</c><00:07:49.240><c> eficiente</c>
máquina da maneira mais eficiente
possível.<00:07:50.440><c> Por</c><00:07:50.599><c> exemplo,</c><00:07:51.080><c> digamos</c><00:07:51.400><c> que</c><00:07:51.479><c> eu</c>
possível. Por exemplo, digamos que eu
preciso<00:07:51.800><c> montar</c><00:07:52.039><c> um</c><00:07:52.159><c> relatório</c><00:07:52.560><c> em</c><00:07:52.759><c> PDF</c><00:07:53.479><c> de</c>
preciso montar um relatório em PDF de
todas<00:07:53.879><c> as</c><00:07:54.039><c> vendas</c><00:07:54.280><c> do</c><00:07:54.440><c> mês.</c><00:07:54.639><c> Vou</c><00:07:54.800><c> fazer</c><00:07:55.039><c> tipo</c>
todas as vendas do mês. Vou fazer tipo
um<00:07:55.360><c> select</c><00:07:55.720><c> asterisco</c><00:07:56.360><c> from</c><00:07:56.759><c> orders</c><00:07:57.280><c> where</c>
um select asterisco from orders where
created<00:07:58.000><c> jet</c><00:07:58.440><c> maior</c><00:07:58.680><c> que</c><00:07:58.840><c> date-</c><00:07:59.479><c> 30.</c><00:08:00.080><c> Essa</c><00:08:00.280><c> é</c>
created jet maior que date- 30. Essa é
uma<00:08:00.560><c> pesquisa</c><00:08:01.000><c> rudimentar</c><00:08:01.879><c> que</c><00:08:02.080><c> filtra</c><00:08:02.560><c> todas</c>
uma pesquisa rudimentar que filtra todas
as<00:08:03.000><c> ordens</c><00:08:03.360><c> criadas</c><00:08:03.759><c> nos</c><00:08:03.960><c> últimos</c><00:08:04.319><c> 30</c><00:08:04.599><c> dias.</c>
as ordens criadas nos últimos 30 dias.
Faz<00:08:05.280><c> de</c><00:08:05.440><c> conta</c><00:08:05.639><c> que</c><00:08:05.759><c> vai</c><00:08:05.879><c> devolver</c><00:08:06.280><c> umas</c><00:08:06.520><c> 500</c>
Faz de conta que vai devolver umas 500
ordens.<00:08:08.000><c> Digamos</c><00:08:08.400><c> que</c><00:08:08.639><c> cada</c><00:08:08.919><c> uma</c><00:08:09.120><c> dessas</c>
ordens. Digamos que cada uma dessas
linhas<00:08:09.879><c> consuma</c><00:08:10.400><c> 500</c><00:08:10.960><c> bytes,</c><00:08:11.639><c> só</c><00:08:12.280><c> KB.</c><00:08:12.879><c> Se</c><00:08:12.960><c> eu</c>
linhas consuma 500 bytes, só KB. Se eu
puxar<00:08:13.400><c> tudo</c><00:08:13.680><c> de</c><00:08:13.840><c> uma</c><00:08:14.000><c> vez</c><00:08:14.199><c> do</c><00:08:14.360><c> banco</c><00:08:14.599><c> e</c><00:08:14.759><c> colocar</c>
puxar tudo de uma vez do banco e colocar
num<00:08:15.240><c> arre</c><00:08:15.520><c> em</c><00:08:15.599><c> memória,</c><00:08:16.120><c> vai</c><00:08:16.280><c> ocupar</c><00:08:16.680><c> 250</c><00:08:17.479><c> MB.</c>
num arre em memória, vai ocupar 250 MB.
É<00:08:18.280><c> bastante</c><00:08:18.759><c> coisa.</c><00:08:19.319><c> Daí</c><00:08:19.560><c> abrimos</c><00:08:19.960><c> uma</c>
É bastante coisa. Daí abrimos uma
biblioteca<00:08:20.680><c> qualquer</c><00:08:21.039><c> para</c><00:08:21.159><c> montar</c><00:08:21.479><c> PDF</c><00:08:22.080><c> e</c>
biblioteca qualquer para montar PDF e
converter<00:08:22.800><c> essas</c><00:08:23.120><c> linhas</c><00:08:23.360><c> em</c><00:08:23.479><c> um</c><00:08:23.599><c> documento</c>
converter essas linhas em um documento
PDF<00:08:24.440><c> em</c><00:08:24.639><c> memória.</c><00:08:25.080><c> Para</c><00:08:25.240><c> simplificar</c><00:08:25.720><c> o</c>
PDF em memória. Para simplificar o
exemplo,<00:08:26.240><c> digamos</c><00:08:26.520><c> que</c><00:08:26.680><c> cada</c><00:08:26.919><c> linha</c><00:08:27.199><c> no</c><00:08:27.440><c> PDF</c>
exemplo, digamos que cada linha no PDF
também<00:08:28.599><c> use</c><00:08:28.840><c> 500</c><00:08:29.199><c> by.</c><00:08:29.520><c> Significa</c><00:08:29.879><c> que</c><00:08:30.000><c> no</c><00:08:30.120><c> fim</c>
também use 500 by. Significa que no fim
da<00:08:30.400><c> operação</c><00:08:30.960><c> eu</c><00:08:31.120><c> vou</c><00:08:31.240><c> estar</c><00:08:31.360><c> consumindo</c><00:08:31.840><c> 500</c>
da operação eu vou estar consumindo 500
MB<00:08:33.039><c> na</c><00:08:33.200><c> memória,</c><00:08:34.200><c> GB,</c><00:08:35.279><c> metade</c><00:08:35.800><c> com</c><00:08:35.959><c> os</c><00:08:36.080><c> dados</c>
MB na memória, GB, metade com os dados
que<00:08:36.440><c> vieram</c><00:08:36.680><c> do</c><00:08:36.839><c> banco</c><00:08:37.039><c> e</c><00:08:37.240><c> metade</c><00:08:37.640><c> com</c><00:08:37.839><c> o</c><00:08:37.919><c> PDF.</c>
que vieram do banco e metade com o PDF.
E<00:08:38.839><c> qual</c><00:08:39.039><c> o</c><00:08:39.120><c> jeito</c><00:08:39.440><c> certo?</c><00:08:40.000><c> Depende.</c><00:08:40.599><c> Talvez</c>
E qual o jeito certo? Depende. Talvez
seja<00:08:41.279><c> esse</c><00:08:41.560><c> mesmo.</c><00:08:42.080><c> Existem</c><00:08:42.560><c> técnicas</c><00:08:43.080><c> se</c>
seja esse mesmo. Existem técnicas se
quiser<00:08:43.640><c> otimizar.</c><00:08:44.519><c> Um</c><00:08:44.680><c> dos</c><00:08:44.920><c> jeitos</c><00:08:45.240><c> é</c>
quiser otimizar. Um dos jeitos é
escolhendo<00:08:45.839><c> uma</c><00:08:46.000><c> biblioteca</c><00:08:46.480><c> de</c><00:08:46.640><c> PDF</c><00:08:47.080><c> que</c>
escolhendo uma biblioteca de PDF que
suporte<00:08:47.839><c> escrever</c><00:08:48.560><c> direto</c><00:08:49.000><c> pro</c><00:08:49.279><c> disco</c><00:08:49.600><c> em</c><00:08:49.800><c> vez</c>
suporte escrever direto pro disco em vez
de<00:08:50.080><c> acumular</c><00:08:50.480><c> tudo</c><00:08:50.680><c> em</c><00:08:50.839><c> memória.</c><00:08:51.320><c> Por</c>
de acumular tudo em memória. Por
exemplo,<00:08:51.760><c> em</c><00:08:51.920><c> Java</c><00:08:52.200><c> tem</c><00:08:52.360><c> a</c><00:08:52.440><c> biblioteca</c><00:08:52.959><c> PDF</c>
exemplo, em Java tem a biblioteca PDF
Box<00:08:53.839><c> da</c><00:08:54.600><c> podemos</c><00:08:54.959><c> ir</c><00:08:55.120><c> salvando</c>
Box da podemos ir salvando
incrementalmente<00:08:56.480><c> uma</c><00:08:56.680><c> página</c><00:08:56.959><c> de</c><00:08:57.120><c> cada</c><00:08:57.320><c> vez</c>
incrementalmente uma página de cada vez
pro<00:08:57.720><c> disco.</c><00:08:58.240><c> Digamos</c><00:08:58.560><c> que</c><00:08:58.760><c> cada</c><00:08:59.040><c> página</c><00:08:59.440><c> tenha</c>
pro disco. Digamos que cada página tenha
20<00:09:00.000><c> ordens,</c><00:09:00.399><c> então</c><00:09:00.600><c> eu</c><00:09:00.720><c> só</c><00:09:00.839><c> vou</c><00:09:01.040><c> precisar</c><00:09:01.560><c> de</c>
20 ordens, então eu só vou precisar de
aproximadamente<00:09:02.600><c> 10</c><00:09:02.880><c> MB</c><00:09:03.399><c> na</c><00:09:03.560><c> memória</c><00:09:03.920><c> por</c>
aproximadamente 10 MB na memória por
vez.<00:09:04.720><c> Além</c><00:09:04.959><c> disso,</c><00:09:05.279><c> podemos</c><00:09:05.600><c> ir</c><00:09:05.760><c> recebendo</c>
vez. Além disso, podemos ir recebendo
uma<00:09:06.440><c> linha</c><00:09:06.720><c> de</c><00:09:06.880><c> cada</c><00:09:07.160><c> vez</c><00:09:07.360><c> do</c><00:09:07.560><c> banco</c><00:09:08.000><c> e</c><00:09:08.200><c> montar</c>
uma linha de cada vez do banco e montar
uma<00:09:08.800><c> linha</c><00:09:09.040><c> no</c><00:09:09.240><c> PDF</c><00:09:09.800><c> e</c><00:09:10.040><c> descartar</c><00:09:10.560><c> essa</c>
uma linha no PDF e descartar essa
memória.<00:09:11.480><c> Daí</c><00:09:11.680><c> eu</c><00:09:11.839><c> recebo</c><00:09:12.120><c> a</c><00:09:12.360><c> próxima</c><00:09:12.839><c> linha</c><00:09:13.240><c> e</c>
memória. Daí eu recebo a próxima linha e
faço<00:09:13.640><c> a</c><00:09:13.800><c> mesma</c><00:09:14.120><c> coisa</c><00:09:14.440><c> sem</c><00:09:14.680><c> acumular</c><00:09:15.120><c> tudo.</c><00:09:15.600><c> Em</c>
faço a mesma coisa sem acumular tudo. Em
resumo,<00:09:16.160><c> significa</c><00:09:16.640><c> que</c><00:09:16.959><c> de</c><00:09:17.160><c> memória</c><00:09:17.519><c> de</c>
resumo, significa que de memória de
trabalho<00:09:18.160><c> precisaria,</c><00:09:18.600><c> no</c><00:09:18.760><c> máximo</c><00:09:19.079><c> tem</c><00:09:19.200><c> uns</c>
trabalho precisaria, no máximo tem uns
10<00:09:19.680><c> MB</c><00:09:20.200><c> para</c><00:09:20.360><c> montar</c><00:09:20.600><c> uma</c><00:09:20.800><c> página</c><00:09:21.000><c> de</c><00:09:21.160><c> PDF</c><00:09:21.760><c> e</c>
10 MB para montar uma página de PDF e
mais<00:09:22.560><c> MB</c><00:09:23.120><c> por</c><00:09:23.279><c> linha</c><00:09:23.519><c> que</c><00:09:23.600><c> eu</c><00:09:23.760><c> recebo</c><00:09:24.000><c> do</c>
mais MB por linha que eu recebo do
servidor<00:09:24.480><c> de</c><00:09:24.640><c> banco</c><00:09:24.880><c> de</c><00:09:25.000><c> dados,</c><00:09:25.240><c> um</c><00:09:25.360><c> total</c><00:09:25.600><c> de</c>
servidor de banco de dados, um total de
10<00:09:26.040><c> M5.</c><00:09:27.040><c> Aí</c><00:09:27.279><c> não</c><00:09:27.519><c> importa</c><00:09:27.880><c> se</c><00:09:27.959><c> o</c><00:09:28.079><c> relatório</c><00:09:28.519><c> vai</c>
10 M5. Aí não importa se o relatório vai
ter<00:09:28.880><c> 100</c><00:09:29.160><c> ordens</c><00:09:29.519><c> ou</c><00:09:29.760><c> 1000</c><00:09:30.040><c> ordens.</c><00:09:30.680><c> sempre</c><00:09:30.959><c> eu</c>
ter 100 ordens ou 1000 ordens. sempre eu
vou<00:09:31.279><c> usar</c><00:09:31.560><c> o</c><00:09:31.800><c> máximo</c><00:09:32.160><c> de</c><00:09:32.399><c> 105</c><00:09:33.200><c> de</c><00:09:33.399><c> cada</c><00:09:33.640><c> vez</c><00:09:33.839><c> e</c>
vou usar o máximo de 105 de cada vez e
não<00:09:34.240><c> 500</c><00:09:34.640><c> MB</c><00:09:35.200><c> para</c><00:09:35.399><c> 500</c><00:09:35.839><c> ordens</c><00:09:36.279><c> ou</c><00:09:36.640><c> 1</c><00:09:36.880><c> GB</c><00:09:37.600><c> se</c>
não 500 MB para 500 ordens ou 1 GB se
for<00:09:38.000><c> mês</c><00:09:38.200><c> de</c><00:09:38.360><c> Natal</c><00:09:38.640><c> e</c><00:09:38.720><c> tiver</c><00:09:39.000><c> 1000</c><00:09:39.240><c> ordens.</c>
for mês de Natal e tiver 1000 ordens.
Esse<00:09:40.240><c> é</c><00:09:40.360><c> o</c><00:09:40.440><c> seu</c><00:09:40.640><c> trabalho</c><00:09:40.959><c> como</c><00:09:41.200><c> programador</c><00:09:41.720><c> e</c>
Esse é o seu trabalho como programador e
encontrar<00:09:42.240><c> o</c><00:09:42.440><c> teto</c><00:09:42.839><c> máximo</c><00:09:43.399><c> que</c><00:09:43.680><c> realmente</c>
encontrar o teto máximo que realmente
precisa<00:09:44.600><c> e</c><00:09:44.800><c> limitar</c><00:09:45.200><c> o</c><00:09:45.320><c> uso</c><00:09:45.560><c> de</c><00:09:45.760><c> recursos.</c><00:09:46.279><c> Só</c>
precisa e limitar o uso de recursos. Só
assim<00:09:46.720><c> é</c><00:09:46.920><c> possível</c><00:09:47.279><c> escalar.</c><00:09:47.880><c> O</c><00:09:48.000><c> jeito</c><00:09:48.279><c> amador</c>
assim é possível escalar. O jeito amador
é<00:09:48.880><c> ir</c><00:09:49.040><c> usando</c><00:09:49.320><c> cada</c><00:09:49.560><c> vez</c><00:09:49.760><c> mais</c><00:09:50.000><c> memória</c><00:09:50.480><c> à</c>
é ir usando cada vez mais memória à
medida<00:09:50.920><c> que</c><00:09:51.040><c> os</c><00:09:51.200><c> dados</c><00:09:51.440><c> vão</c><00:09:51.600><c> aumentando</c><00:09:52.000><c> de</c>
medida que os dados vão aumentando de
volume.<00:09:52.880><c> Sempre</c><00:09:53.320><c> pense</c><00:09:53.560><c> em</c><00:09:53.720><c> jeitos</c><00:09:54.000><c> de</c><00:09:54.160><c> usar</c>
volume. Sempre pense em jeitos de usar
um<00:09:54.640><c> teto</c><00:09:55.000><c> fixo</c><00:09:55.360><c> de</c><00:09:55.560><c> memória</c><00:09:55.839><c> e</c><00:09:55.959><c> processamento,</c>
um teto fixo de memória e processamento,
independente<00:09:57.279><c> de</c><00:09:57.519><c> quantos</c><00:09:57.920><c> dados</c><00:09:58.279><c> vai</c>
independente de quantos dados vai
processar.<00:09:59.279><c> Quando</c><00:09:59.519><c> falamos</c><00:09:59.839><c> que</c><00:10:00.000><c> é</c>
processar. Quando falamos que é
importante<00:10:01.000><c> entender</c><00:10:01.600><c> SQL</c><00:10:02.120><c> direito,</c>
importante entender SQL direito,
primeiro<00:10:03.200><c> é</c><00:10:03.399><c> para</c><00:10:03.600><c> aprender</c><00:10:03.920><c> a</c><00:10:04.079><c> fazer</c><00:10:04.360><c> queries</c>
primeiro é para aprender a fazer queries
ou<00:10:05.079><c> pesquisas</c><00:10:05.959><c> selects</c><00:10:06.480><c> que</c><00:10:06.640><c> devolvam</c><00:10:07.120><c> a</c>
ou pesquisas selects que devolvam a
menor<00:10:07.720><c> quantidade</c><00:10:08.320><c> de</c><00:10:08.519><c> dados</c><00:10:08.880><c> quanto</c>
menor quantidade de dados quanto
possível,<00:10:09.680><c> porque</c><00:10:10.000><c> cada</c><00:10:10.360><c> dado</c><00:10:10.839><c> extra</c><00:10:11.040><c> que</c>
possível, porque cada dado extra que
vier<00:10:11.440><c> e</c><00:10:11.600><c> não</c><00:10:11.760><c> usar,</c><00:10:12.279><c> vai</c><00:10:12.560><c> desperdiçar</c><00:10:13.120><c> memória</c>
vier e não usar, vai desperdiçar memória
e<00:10:13.560><c> processamento.</c><00:10:14.240><c> Nós</c><00:10:14.399><c> também</c><00:10:14.640><c> precisamos</c>
e processamento. Nós também precisamos
entender<00:10:15.440><c> algumas</c><00:10:15.760><c> noções,</c><00:10:16.480><c> como</c><00:10:16.920><c> se</c><00:10:17.120><c> vamos</c>
entender algumas noções, como se vamos
escrever<00:10:18.120><c> ou</c><00:10:18.360><c> atualizar</c><00:10:18.959><c> dados.</c>
