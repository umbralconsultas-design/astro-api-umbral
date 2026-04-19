/*************************************
 ASTRO.gs (FINAL FUNCIONAL CON /carta)
*************************************/
function obtenerContextoAstrologico(email) {
  try {

    const datos = obtenerDatosCliente(email);

    if (!datos || !datos.year) {
      return "No disponible";
    }

    // 🔥 ENDPOINT REAL DE TU BACKEND
    const url = "https://astro-api-umbral.onrender.com/carta";

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

    Logger.log("PAYLOAD ASTRO:");
    Logger.log(JSON.stringify(payload));

    const response = UrlFetchApp.fetch(url, {
      method: "post",
      contentType: "application/json",
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    });

    const status = response.getResponseCode();
    const text = response.getContentText();

    Logger.log("STATUS ASTRO: " + status);
    Logger.log("RESPUESTA CRUDA:");
    Logger.log(text);

    if (status !== 200) {
      Logger.log("⚠️ ERROR BACKEND ASTRO");
      return "No disponible";
    }

    let result;

    try {
      result = JSON.parse(text);
    } catch (e) {
      Logger.log("⚠️ RESPUESTA NO ES JSON");
      return "No disponible";
    }

    Logger.log("RESPUESTA ASTRO PARSEADA:");
    Logger.log(JSON.stringify(result));

    return JSON.stringify(result);

  } catch (error) {

    Logger.log("ERROR ASTRO: " + error.message);

    return "No disponible";
  }
}
