plot.ts(song_example.III, col="#ff000080")
lines(example.III.song, col="#0000ff80")
lines(example.III.song.dat, col="#00ff0080")

plot.ts(alpha.beta.1$alpha, col="red", ylim=c(-1,2.7), ylab="alpha/beta value", main="red: alpha, blue: beta")
lines(alpha.beta.1$beta, col="blue")

for (i in names(synth_debug.c)) {
  if (length(unique(synth_debug.c[,i])) == 1)
    print(i)
}

