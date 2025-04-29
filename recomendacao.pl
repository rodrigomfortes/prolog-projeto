% Carregar a base de dados
:- consult('dados.pl').

:- dynamic assistido/2.
:- dynamic filme/2.
:- dynamic serie/2.
:- dynamic anime/2.
:- dynamic nota/2.

% Recomendação de filmes, séries e animes com base em gênero e nota
recomendar(Gostos, Filme, Nota) :-
    filme(Filme, Genero),
    nota(Filme, Nota),
    member(Genero, Gostos),
    \+ assistido(filme, Filme).  % Verifica se o filme não foi assistido

recomendar_serie(Gostos, Serie, Nota) :-
    serie(Serie, Genero),
    nota(Serie, Nota),
    member(Genero, Gostos),
    \+ assistido(serie, Serie).  % Verifica se a série não foi assistida

recomendar_anime(Gostos, Anime, Nota) :-
    anime(Anime, Genero),
    nota(Anime, Nota),
    member(Genero, Gostos),
    \+ assistido(anime, Anime).  % Verifica se o anime não foi assistido

% Top 3 filmes baseados no gosto do usuário (ordenado por nota, do maior para o menor)
top_3_filmes(Gostos, Top3) :-
    findall([Filme, Nota], recomendar(Gostos, Filme, Nota), Filmes),
    sort(2, @=<, Filmes, FilmesOrdenados),  % Ordena pelo segundo elemento (Nota), do maior para o menor
    remove_duplicados(FilmesOrdenados, [], FilmesSemDuplicatas),
    first_n(3, FilmesSemDuplicatas, Top3).

% Top 3 séries baseadas no gosto do usuário (ordenado por nota, do maior para o menor)
top_3_series(Gostos, Top3) :-
    findall([Serie, Nota], recomendar_serie(Gostos, Serie, Nota), Series),
    sort(2, @=<, Series, SeriesOrdenadas),  % Ordena pelo segundo elemento (Nota), do maior para o menor
    remove_duplicados(SeriesOrdenadas, [], SeriesSemDuplicatas),
    first_n(3, SeriesSemDuplicatas, Top3).

% Top 3 animes baseados no gosto do usuário (ordenado por nota, do maior para o menor)
top_3_animes(Gostos, Top3) :-
    findall([Anime, Nota], recomendar_anime(Gostos, Anime, Nota), Animes),
    sort(2, @=<, Animes, AnimesOrdenados),  % Ordena pelo segundo elemento (Nota), do maior para o menor
    remove_duplicados(AnimesOrdenados, [], AnimesSemDuplicatas),
    first_n(3, AnimesSemDuplicatas, Top3).

% Auxiliar para pegar os 3 primeiros filmes, séries ou animes da lista ordenada
first_n(N, [X|T], [X|Result]) :- 
    N > 0,  
    N1 is N - 1,  
    first_n(N1, T, Result).  

% Caso N seja 0, retorne uma lista vazia
first_n(0, _, []).

% Função para remover duplicados da lista
remove_duplicados([], Result, Result).  % Caso base: lista vazia, retorna a lista de resultados final
remove_duplicados([H|T], Result, FinalResult) :-
    % Verifica se o conteúdo H já está na lista de resultados
    (member(H, Result) -> remove_duplicados(T, Result, FinalResult) ; remove_duplicados(T, [H|Result], FinalResult)).

% Marcar filme, série ou anime como assistido
marcar_assistido(Filme) :- 
    filme(Filme, _), 
    assert(assistido(filme, Filme)).

marcar_assistido(Serie) :- 
    serie(Serie, _), 
    assert(assistido(serie, Serie)).

marcar_assistido(Anime) :- 
    anime(Anime, _), 
    assert(assistido(anime, Anime)).

% Consultar filmes assistidos
assistidos_filmes(ListaFilmes) :-
    findall(Filme, assistido(filme, Filme), ListaFilmes).

% Consultar séries assistidas
assistidos_series(ListaSeries) :-
    findall(Serie, assistido(serie, Serie), ListaSeries).

% Consultar animes assistidos
assistidos_animes(ListaAnimes) :-
    findall(Anime, assistido(anime, Anime), ListaAnimes).
