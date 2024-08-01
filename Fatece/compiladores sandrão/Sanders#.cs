Lista[];
Console.WriteLine("escreva seu nome: ");
Console.ReadLine(nome);
For(i=0; i<4; i++)
{
    Console.WriteLine("Digite sua nota, valor decimal");
    Console.ReadLine(valor);
    Lista.add(valor);
}
Media = lista[0] + lista[1] + lista[2] + lista[3];
Media = media / 4;
if(media >= 5)
{
    Console.WriteLine(nome + " você passou de ano nengue e sua media é " + media);
}
Else
{
    Console.WriteLine(nome + " você é burro nengue e sua media é " + media);
}
