using System.Runtime.Serialization;
using heart.utils;

namespace heart.db
{
	[DataContract]
	internal class User: Data<User>
	{
		[DataMember(Name = "login", Order = 1, EmitDefaultValue = false)] public string Login;
		[DataMember(Name = "passhash", Order = 1, EmitDefaultValue = false)] public string PassHash;
		[DataMember(Name = "expr", Order = 1, EmitDefaultValue = false)] public string Expression;
		[DataMember(Name = "readable", Order = 1, EmitDefaultValue = false)] public string Readable;
	}
}