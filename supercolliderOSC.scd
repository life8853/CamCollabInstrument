
(
~clock = TempoClock.new(2.0);
~instrument = \bd;
~sampleNumber = 22;
~note = 60;
~reverbOn = false;

~pattern = Pbind(
	\type, \dirt,
	\dirt, ~dirt,
	\s, Pfunc{~instrument},
	\n, Pfunc{~sampleNumber},
	\midinote, Pfunc{~note},
    \dur, 1,
	\amp, 1,

	//reverb
	\size,   0.2,
	\room,   Pfunc {~reverbOn.if({0.5}, {0.0})},
    \dry,    Pfunc {~reverbOn.if({0.7}, {0.0})}
);

~player = ~pattern.play().stop();


OSCdef.new(
	\startpattern,
	{|msg, time, addr, recvPort|
		~player.play()
	},
	'/startpattern'
);

OSCdef.new(
	\stoppattern,
	{|msg, time, addr, recvPort|
		~player.stop()
	},
	'/stoppattern'
);


OSCdef.new(
	\changeInstrument,
	{|msg, time, addr, recvPort|
		~instrument = msg[1].asSymbol;
		~sampleNumber =msg[2].asInteger;
	},
	'/changeinstrument'
);

OSCdef.new(
	\setNote,
	{|msg, time, addr, recvPort|
		~note = msg[1].asInteger;
	},
	'/setnote'
);


OSCdef.new(
	\setReverb,
	{|msg, time, addr, recvPort|
		~reverbOn = msg[1].asBoolean;
	},
	'/setreverb'
);


)

(
Pbind(
    \type,      \dirt,         // use the SuperDirt event handler
    \dirt,      ~dirt,         // your SuperDirt instance
	\s, \superpiano,  // synth name
    \midinote,  Pseq([60,62,64,65,67,69,71,72], inf),
    \dur,       0.5,           // half-beat per note
    \amp,       0.5,
    \sustain,   0.4            // note length (beats)
).play();
)