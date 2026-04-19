/*************************************
 ASTRO.gs (FINAL CON TEXTO INTERPRETABLE)
*************************************/
function obtenerContextoAstrologico(email) {
  try {

    const datos = obtenerDatosCliente(email);

    if (!datos || !datos.year) {
      return "No disponible";
    }

    const url = "https://astro-api-umbral-1.onrender.com/carta";

    const payload = {
      name: datos.nombre || "Usuario",
      year: parseInt(datos.year),
      month: parseInt(datos.month),
      day: parseInt(datos.day),
      hour: parseInt(datos.hour),
      minute: parseInt(datos.minute),
      lat: 19.4326,
      lon: -99.1332,
      timezone: -6
    };

    const response = UrlFetchApp.fetch(url, {
      method: "post",
      contentType: "application/json",
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    });

    const text = response.getContentText();

    const parsed = JSON.parse(text);

    if (!parsed.carta) {
      return "No disponible";
    }

    const c = parsed.carta;

    // 🔥 CONVERTIR A TEXTO PARA IA
    const resumen = `
Carta natal del usuario:

Sol en ${c.sol.signo}
Luna en ${c.luna.signo}
Ascendente en ${c.ascendente.signo}
Mercurio en ${c.mercurio.signo}
Venus en ${c.venus.signo}
Marte en ${c.marte.signo}
`;

    return resumen;

  } catch (error) {
    Logger.log("ERROR ASTRO: " + error.message);
    return "No disponible";
  }
}
