package info.bliki.api;

import org.xml.sax.Attributes;
import org.xml.sax.SAXException;

/**
 * Reads <code>User</code> data from an XML file generated by the <a href="http://meta.wikimedia.org/w/api.php">Wikimedia API</a>
 */
public class XMLUserParser extends AbstractXMLParser {
	private static final String LOGIN_ID = "login";

	private static final String RESULT_ID = "result";

	private static final String USER_ID = "lguserid";

	private static final String USER_NAME_ID = "lgusername";

	private static final String LG_TOKEN_ID = "lgtoken";

	private static final String TOKEN_ID = "token";

	private User fUser;

	public XMLUserParser(User user, String xmlText) throws SAXException {
		super(xmlText);
		fUser = user;
	}

	@Override
	public void startElement(String namespaceURI, String localName, String qName, Attributes atts) {
		fAttributes = atts;

		if (LOGIN_ID.equals(qName)) {
            String result = fAttributes.getValue(RESULT_ID);
            if (result.equalsIgnoreCase(User.NEED_TOKEN_ID)) {
                fUser.setResult(fAttributes.getValue(RESULT_ID));
                fUser.setToken(fAttributes.getValue(TOKEN_ID));
            } else {
                fUser.setResult(fAttributes.getValue(RESULT_ID));
                fUser.setUserid(fAttributes.getValue(USER_ID));
                fUser.setNormalizedUsername(fAttributes.getValue(USER_NAME_ID));
                fUser.setToken(fAttributes.getValue(LG_TOKEN_ID));
            }
//			System.out.println(fUser.toString());
		}
		fData = null;
	}

	@Override
	public void endElement(String uri, String name, String qName) {
		try {
			if (LOGIN_ID.equals(qName)) {

			}

			fData = null;
			fAttributes = null;

		} catch (RuntimeException re) {
			re.printStackTrace();
		}
	}

}
