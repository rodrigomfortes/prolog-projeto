:- dynamic assistido/1.

% Filmes e gêneros
filme(interestelar, ficcao).
filme(matrix, acao).
filme(harry_potter, fantasia).
filme(jurassic_park, aventura).

% Recomendação de filmes
recomendar(Gostos, Filme) :-
    filme(Filme, Genero),
    member(Genero, Gostos),
    \+ assistido(Filme).

% Marcar filme como assistido
marcar_assistido(Filme) :-
    assert(assistido(Filme)).
