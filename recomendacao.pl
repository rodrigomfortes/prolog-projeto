% Carregar a base de dados
:- consult('dados.pl').

:- dynamic assistido/1.
:- dynamic assistido/2.
:- discontiguous filme/2.
:- discontiguous serie/2.
:- discontiguous anime/2.
:- discontiguous nota/2.

% Recomendação de filmes, séries e animes com base em gênero e nota
recomendar(Gostos, Filme, Nota) :-
    filme(Filme, Genero),
    nota(Filme, Nota),
    member(Genero, Gostos),
    \+ assistido(Filme).

recomendar_serie(Gostos, Serie, Nota) :-
    serie(Serie, Genero),
    nota(Serie, Nota),
    member(Genero, Gostos),
    \+ assistido(Serie).

recomendar_anime(Gostos, Anime, Nota) :-
    anime(Anime, Genero),
    nota(Anime, Nota),
    member(Genero, Gostos),
    \+ assistido(Anime).

% Top 3 filmes baseados no gosto do usuário
top_3_filmes(Gostos, Top3) :-
    findall([Filme, Nota], recomendar(Gostos, Filme, Nota), Filmes),
    sort(2, @>=, Filmes, FilmesOrdenados),
    first_n(3, FilmesOrdenados, Top3).

% Top 3 séries baseadas no gosto do usuário
top_3_series(Gostos, Top3) :-
    findall([Serie, Nota], recomendar_serie(Gostos, Serie, Nota), Series),
    sort(2, @>=, Series, SeriesOrdenadas),
    first_n(3, SeriesOrdenadas, Top3).

% Top 3 animes baseados no gosto do usuário
top_3_animes(Gostos, Top3) :-
    findall([Anime, Nota], recomendar_anime(Gostos, Anime, Nota), Animes),
    sort(2, @>=, Animes, AnimesOrdenados),
    first_n(3, AnimesOrdenados, Top3).

% Auxiliar para pegar os 3 primeiros filmes, séries ou animes da lista ordenada
first_n(N, [X|T], [X|Result]) :- 
    N > 0,  
    N1 is N - 1,  
    first_n(N1, T, Result).  

% Caso N seja 0, retorne uma lista vazia
first_n(0, _, []).

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
