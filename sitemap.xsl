<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:s="http://www.sitemaps.org/schemas/sitemap/0.9">
  <xsl:template match="/">
    <html lang="fr">
      <head>
        <title>Sitemap - La Grange des Balas</title>
        <style>
          body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #F8F7F4;
            color: #333;
            padding: 2rem;
            max-width: 1000px;
            margin: 0 auto;
          }
          h1 { color: #15803d; }
          p { color: #555; }
          table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 2rem;
            background-color: white;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
          }
          th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #ddd;
          }
          th {
            background-color: #15803d;
            color: white;
            font-weight: 600;
          }
          tr:hover { background-color: #f1f5f9; }
          a { color: #15803d; text-decoration: none; }
          a:hover { text-decoration: underline; }
        </style>
      </head>
      <body>
        <h1>Sitemap XML</h1>
        <p>Ce fichier est utilisé par les moteurs de recherche (comme Google) pour explorer plus facilement les pages du site.</p>
        
        <table>
          <thead>
            <tr>
              <th>URL de la page</th>
              <th>Dernière modification</th>
              <th>Fréquence</th>
              <th>Priorité</th>
            </tr>
          </thead>
          <tbody>
            <xsl:for-each select="s:urlset/s:url">
              <tr>
                <td>
                  <a href="{s:loc}" target="_blank">
                    <xsl:value-of select="s:loc"/>
                  </a>
                </td>
                <td><xsl:value-of select="s:lastmod"/></td>
                <td><xsl:value-of select="s:changefreq"/></td>
                <td><xsl:value-of select="s:priority"/></td>
              </tr>
            </xsl:for-each>
          </tbody>
        </table>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>