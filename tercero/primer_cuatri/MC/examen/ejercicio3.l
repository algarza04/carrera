car [a-zA-Z]
digito [0-9]
cardigito [a-zA-Z0-9]
sec ({car}+)
var ({car}{cardigito}*)
email ({var}\@({sec}\.)?{sec}\.{sec})
	int i = 0;
	
%%
{email} {i++;printf("Email: %s\n",yytext);}
.|\n {;}
%%

int yywrap(){}

int main(){
	yylex();
	{printf("Num. de emails %d\n", i);}
	return 1;
}
