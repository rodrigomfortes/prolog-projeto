:- consult('bases.pl').  % Carregar a base de filmes de 'bases.pl'

% Recomendação baseada nos gêneros
recomendar_filmes(Generos, Recomendacoes) :-
    findall([Titulo, Nota],
            (filme(Titulo, GenerosFilme, Nota), intersection(Generos, GenerosFilme, _)),
            Recomendacoes).

% Exemplo de marcação de filmes assistidos
marcar_assistido(Titulo) :-
    retract(filme(Titulo, Generos, Nota)),
    assert(filme(Titulo, Generos, Nota)).

% Servidor HTTP (exemplo com HTTP server do Prolog)
:- use_module(library(http/http_server)).
:- use_module(library(http/http_parameters)).

server :-
    http_server([port(8080)]).

% Endpoint de recomendação
:- http_handler('/recommend', recommend_handler, []).

recommend_handler(Request) :-
    http_parameters(Request, [genres(Genres, [list])]),
    recomendar_filmes(Genres, Recomendacoes),
    format('Content-Type: application/json~n~n'),
    atom_json_term(Response, Recomendacoes, []),
    write(Response).

% Endpoint de marcação como assistido
:- http_handler('/markWatched', mark_watched_handler, []).

mark_watched_handler(Request) :-
    http_parameters(Request, [id(Id, [])]),
    marcar_assistido(Id),
    format('Content-Type: application/json~n~n'),
    write('{"status": "success"}').
