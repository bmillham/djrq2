# encoding: cinje

: from cinje.std.html import link

: def navbar
	<div style="text-align: center"><span style="border:1px solid red;">
	: using link "/album/letters"
		Browse By Album Letters
	: end
	&nbsp;
	: using link "/artist/letters"
		Browse By Artist Letters
	: end
	</span></div>
: end

