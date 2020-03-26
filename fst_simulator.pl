% FST_Simulator.pl
% 185:416 Minds, Machines & Computation
%
% Simulates an FST.
% Example Query: fst([a,a,b,b],Output).
%
% This simulator assumes that an FST definition has been
% loaded, using the following predicates:
% initial_state(q)
% accepting_state(a)
% t(b,a,i,o)    transition from a to b, inputting i, outputting o

% Set some Prolog options.
% Changing max_depth from default 10 to 0 means it will write out
% the full tree no matter how deep. The other options remain at
% their default values, but will disappear if not repeated here.

:- set_prolog_flag(answer_write_options,[quoted(true),portray(true),
       max_depth(0),spacing(next_argument)]).

% Top-level predicate

fst(I,O) :-
	initial_state(Q1),
	accept(Q1,I,O,[],Steps),
	write_steps([[Q1,I,[]]|Steps]).

% Conditions for an accepting operation.

accept(Q1,[I|IRest],[O|ORest],OAccum,[[Q2,IRest,OMore]|RestSteps]) :-
	t(Q1,Q2,I,O),
	I \= nil, O \= nil,
	append(OAccum,[O],OMore),
	accept(Q2,IRest,ORest,OMore,RestSteps).

accept(Q1,[I|IRest],OAll,OAccum,[[Q2,IRest,OAccum]|RestSteps]) :-
	t(Q1,Q2,I,nil),
	I \= nil,
	accept(Q2,IRest,OAll,OAccum,RestSteps).

accept(Q1,IAll,[O|ORest],OAccum,[[Q2,IAll,OMore]|RestSteps]) :-
	t(Q1,Q2,nil,O),
	O \= nil,
	append(OAccum,[O],OMore),
	accept(Q2,IAll,ORest,OMore,RestSteps).

accept(Q,[],[],_,[]) :- accepting_state(Q).

% Write out the steps

write_steps([]).
write_steps([Step|Rest]) :-
	write_config(Step), nl,
	write_steps(Rest).

write_config([Q,Input,Output]) :-
	write(Q), write(" "), write(Input), write(" "), write(Output).